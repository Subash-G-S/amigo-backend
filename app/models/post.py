from sqlalchemy import Column, String, Text, DateTime
from app.database.database import Base
from datetime import datetime
from sqlalchemy import Boolean

class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_anonymous = Column(
        Boolean,
        default=False
    )