from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String

from app.database.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(
        String,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
    )

    post_id = Column(
        String,
        ForeignKey("posts.id"),
    )

    content = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
