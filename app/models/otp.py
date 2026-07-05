from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from app.database.database import Base


class OTP(Base):
    __tablename__ = "otps"

    id = Column(String, primary_key=True)

    email = Column(
        String,
        nullable=False,
        index=True,
    )

    otp = Column(
        String,
        nullable=False,
    )

    expires_at = Column(
        DateTime,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
