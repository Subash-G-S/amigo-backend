import random

from app.services.redis_otp_service import (
    delete_otp,
    get_otp,
)
from app.services.redis_otp_service import save_otp as redis_save_otp


def generate_otp():
    return str(random.randint(100000, 999999))


def save_otp(email: str):
    otp = generate_otp()

    redis_save_otp(email, otp)

    return otp


def verify_otp(
    email: str,
    otp: str,
):
    stored_otp = get_otp(email)

    if stored_otp is None:
        return False

    if stored_otp != otp:
        return False

    delete_otp(email)

    return True
