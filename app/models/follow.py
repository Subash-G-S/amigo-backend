from sqlalchemy import Column, String, ForeignKey, DateTime
from datetime import datetime

from app.database.database import Base



class Follow(Base):
    __tablename__ = "follows"

    id = Column(
        String,
        primary_key=True,
        index=True,
    )

    follower_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
    )

    following_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )