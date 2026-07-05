from app.services.redis_service import redis_client

OTP_EXPIRY = 300  # 5 minutes


def save_otp(email: str, otp: str):
    redis_client.setex(
        f"otp:{email}",
        OTP_EXPIRY,
        otp,
    )


def get_otp(email: str):
    return redis_client.get(f"otp:{email}")


def delete_otp(email: str):
    redis_client.delete(f"otp:{email}")
