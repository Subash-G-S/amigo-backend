import os
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.follow import Follow
from app.models.post import Post
from app.models.user import User
from app.schemas.profile_schema import UpdateProfile
from app.schemas.user_schema import (
    ForgotPasswordRequest,
    LoginUser,
    RegisterUser,
    ResetPasswordRequest,
    VerifyOTPRequest,
)
from app.services.jwt_service import create_access_token
from app.services.mail_service import send_otp_email
from app.services.otp_service import save_otp, verify_otp
from app.services.security import hash_password, verify_password

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
router = APIRouter()


@router.post("/register")
def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        id=str(uuid4()),
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
    )

    db.add(new_user)
    db.commit()

    return {"success": True, "message": "Account created successfully."}


@router.post("/login")
def login_user(user: LoginUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    valid_password = verify_password(user.password, existing_user.password)

    if not valid_password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(existing_user.id)

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": existing_user.id,
            "name": existing_user.name,
            "email": existing_user.email,
        },
    }


security = HTTPBearer()


@router.get("/me")
def get_me(credentials=Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload["sub"]

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "success": True,
            "user": {"id": user.id, "name": user.name, "email": user.email},
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/check-email/{email}")
def check_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    return {"available": user is None}


@router.get("/health")
def health():
    return {"status": "online", "service": "AMIGO API"}


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email.")

    otp = save_otp(request.email)
    send_otp_email(
        request.email,
        otp,
    )

    return {"success": True, "message": "OTP sent successfully."}


@router.post("/verify-otp")
def verify_otp_route(
    request: VerifyOTPRequest,
    db: Session = Depends(get_db),
):
    valid = verify_otp(
        request.email,
        request.otp,
    )

    if not valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

    return {"success": True, "message": "OTP verified."}


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    valid = verify_otp(
        db,
        request.email,
        request.otp,
    )

    if not valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.password = hash_password(request.new_password)

    db.commit()

    return {"success": True, "message": "Password reset successfully."}


@router.get("/search")
def search_users(
    q: str,
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .filter(
            or_(
                User.name.ilike(f"%{q}%"),
                User.email.ilike(f"%{q}%"),
            )
        )
        .all()
    )

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
        for user in users
    ]


@router.get("/user/{user_id}")
def get_user_profile(
    user_id: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    posts = db.query(func.count(Post.id)).filter(Post.user_id == user.id).scalar()
    followers = (
        db.query(func.count(Follow.id)).filter(Follow.following_id == user.id).scalar()
    )
    following = (
        db.query(func.count(Follow.id)).filter(Follow.follower_id == user.id).scalar()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "posts": posts,
        "followers": followers,
        "following": following,
    }


@router.get("/profile")
def my_profile(
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

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    posts = db.query(func.count(Post.id)).filter(Post.user_id == user.id).scalar()

    followers = (
        db.query(func.count(Follow.id)).filter(Follow.following_id == user.id).scalar()
    )

    following = (
        db.query(func.count(Follow.id)).filter(Follow.follower_id == user.id).scalar()
    )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "bio": user.bio or "",
        "posts": posts,
        "followers": followers,
        "following": following,
    }


@router.put("/profile")
def update_profile(
    data: UpdateProfile,
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

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.name = data.name
    user.bio = data.bio

    db.commit()

    return {"message": "Profile updated successfully"}
