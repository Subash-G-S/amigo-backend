from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.like import Like
from app.models.post import Post

security = HTTPBearer()
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter()

@router.post("/{post_id}/like")
def like_post(
    post_id: str,
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
            detail="Invalid Token",
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

    existing = (
        db.query(Like)
        .filter(
            Like.user_id == user_id,
            Like.post_id == post_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already liked",
        )

    like = Like(
        id=str(uuid4()),
        user_id=user_id,
        post_id=post_id,
    )

    db.add(like)
    db.commit()

    return {
        "message": "Post liked",
    }
@router.delete("/{post_id}/like")
def unlike_post(
    post_id: str,
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
            detail="Invalid Token",
        )

    like = (
        db.query(Like)
        .filter(
            Like.user_id == user_id,
            Like.post_id == post_id,
        )
        .first()
    )

    if not like:
        raise HTTPException(
            status_code=404,
            detail="Like not found",
        )

    db.delete(like)
    db.commit()

    return {
        "message": "Post unliked",
    }