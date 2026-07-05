from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.follow import Follow
from app.models.user import User
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()


@router.post("/{user_id}")
def follow_user(
    user_id: str,
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

    if current_user == user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot follow yourself.",
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    existing = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user,
            Follow.following_id == user_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already following",
        )

    follow = Follow(
        id=str(uuid4()),
        follower_id=current_user,
        following_id=user_id,
    )

    db.add(follow)
    db.commit()

    return {
        "success": True,
        "message": "User followed",
    }
@router.delete("/{user_id}")
def unfollow_user(
    user_id: str,
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

    follow = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user,
            Follow.following_id == user_id,
        )
        .first()
    )

    if not follow:
        raise HTTPException(
            status_code=404,
            detail="Follow not found",
        )

    db.delete(follow)
    db.commit()

    return {
        "success": True,
        "message": "User unfollowed",
    }
@router.get("/is-following/{user_id}")
def is_following(
    user_id: str,
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

    follow = (
        db.query(Follow)
        .filter(
            Follow.follower_id == current_user,
            Follow.following_id == user_id,
        )
        .first()
    )

    return {
        "following": follow is not None
    }
@router.get("/followers/{user_id}")
def get_followers(
    user_id: str,
    db: Session = Depends(get_db),
):

    followers = (
        db.query(User)
        .join(
            Follow,
            Follow.follower_id == User.id,
        )
        .filter(
            Follow.following_id == user_id,
        )
        .all()
    )

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "bio": user.bio,
        }
        for user in followers
    ]
@router.get("/following/{user_id}")
def get_following(
    user_id: str,
    db: Session = Depends(get_db),
):

    following = (
        db.query(User)
        .join(
            Follow,
            Follow.following_id == User.id,
        )
        .filter(
            Follow.follower_id == user_id,
        )
        .all()
    )

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "bio": user.bio,
        }
        for user in following
    ]