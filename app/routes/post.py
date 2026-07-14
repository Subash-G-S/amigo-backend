import os
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.comment import Comment
from app.models.like import Like
from app.models.post import Post
from app.models.user import User
from app.schemas.post_schema import CreatePost

router = APIRouter()


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


security = HTTPBearer()


@router.post("/create")
def create_post(
    post: CreatePost, credentials=Security(security), db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload["sub"]

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_post = Post(
        id=str(uuid4()),
        user_id=user_id,
        content=post.content,
        is_anonymous=post.is_anonymous,
    )

    db.add(new_post)
    db.commit()

    return {"message": "Post created successfully"}


@router.get("/feed")
def get_feed(credentials=Security(security), db: Session = Depends(get_db)):

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        current_user = payload["sub"]

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    posts = (
        db.query(Post, User)
        .join(User, User.id == Post.user_id)
        .order_by(Post.created_at.desc())
        .all()
    )

    feed = []

    for post, user in posts:

        like_count = (
            db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
        )

        liked = (
            db.query(Like)
            .filter(
                Like.post_id == post.id,
                Like.user_id == current_user,
            )
            .first()
            is not None
        )

        feed.append(
            {
                "id": post.id,
                "author": user.name,
                "content": post.content,
                "created_at": post.created_at,
                "likes": like_count,
                "liked": liked,
                "is_anonymous": post.is_anonymous,
            }
        )

    return feed


@router.get("/me")
def get_my_posts(
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

        current_user = payload["sub"]

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token",
        )

    posts = (
        db.query(Post, User)
        .join(User, User.id == Post.user_id)
        .filter(Post.user_id == current_user)
        .order_by(Post.created_at.desc())
        .all()
    )
    my_posts = []

    for post, user in posts:
        like_count = (
            db.query(func.count(Like.id)).filter(Like.post_id == post.id).scalar()
        )

        liked = (
            db.query(Like)
            .filter(
                Like.post_id == post.id,
                Like.user_id == current_user,
            )
            .first()
            is not None
        )

        comment_count = (
            db.query(func.count(Comment.id)).filter(Comment.post_id == post.id).scalar()
        )

        my_posts.append(
            {
                "id": post.id,
                "author": user.name,
                "content": post.content,
                "created_at": post.created_at,
                "likes": like_count,
                "comments": comment_count,
                "liked": liked,
                "is_anonymous": post.is_anonymous,
            }
        )

    return posts
