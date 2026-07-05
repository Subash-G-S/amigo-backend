import re

from pydantic import BaseModel, EmailStr, field_validator


class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_amrita_email(cls, value):
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]*students\.amrita\.edu$"

        if not re.match(pattern, value):
            raise ValueError("Only Amrita student email addresses are allowed.")

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        pattern = (
            r"^(?=.*[a-z])"
            r"(?=.*[A-Z])"
            r"(?=.*\d)"
            r"(?=.*[@$!%*?&])"
            r"[A-Za-z\d@$!%*?&]{8,}$"
        )

        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter, "
                "one number and one special character."
            )

        return value


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
