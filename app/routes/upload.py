import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, HTTPException, Security, UploadFile
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.services.cloudinary_service import upload_profile_image

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(prefix="/upload", tags=["Upload"])

security = HTTPBearer()


@router.put("/profile-photo")
async def upload_profile_photo(
    image: UploadFile = File(...),
    credentials=Security(security),
    db: Session = Depends(get_db),
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed.",
        )

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

    image_url = upload_profile_image(image.file)

    user.profile_picture = image_url

    db.commit()

    return {
        "success": True,
        "profile_picture": image_url,
    }