from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.models.user import User

from app.database.database import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment_schema import CreateComment

router = APIRouter()

security = HTTPBearer()

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@router.post("/create/{post_id}")
def create_comment(
    post_id: str,
    comment: CreateComment,
    credentials=Security(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload["sub"]

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    new_comment = Comment(
        id=str(uuid4()),
        user_id=user_id,
        post_id=post_id,
        content=comment.content,
    )

    db.add(new_comment)
    db.commit()

    return {
        "message": "Comment added successfully"
    }
@router.get("/{post_id}")
def get_comments(
    post_id: str,
    db: Session = Depends(get_db),
):

    comments = (
        db.query(Comment, User)
        .join(User, User.id == Comment.user_id)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

    response = []

    for comment, user in comments:

        response.append({
            "id": comment.id,
            "author": user.name,
            "content": comment.content,
            "created_at": comment.created_at,
        })

    return response