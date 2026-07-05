import random
from datetime import datetime, timedelta
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.otp import OTP


def generate_otp():
    return str(random.randint(100000, 999999))


def save_otp(
    db: Session,
    email: str,
):
    # Delete previous OTPs
    db.query(OTP).filter(
        OTP.email == email
    ).delete()

    otp = generate_otp()

    new_otp = OTP(
        id=str(uuid4()),
        email=email,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    )

    db.add(new_otp)
    db.commit()

    return otp


def verify_otp(
    db: Session,
    email: str,
    otp: str,
):
    record = (
        db.query(OTP)
        .filter(
            OTP.email == email,
            OTP.otp == otp,
        )
        .first()
    )

    if not record:
        return False

    if record.expires_at < datetime.utcnow():
        db.delete(record)
        db.commit()
        return False

    return True