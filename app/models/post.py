from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String, Text

from app.database.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_anonymous = Column(Boolean, default=False)
