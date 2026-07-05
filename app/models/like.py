from sqlalchemy import Column, ForeignKey, String

from app.database.database import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(String, primary_key=True, index=True)

    user_id = Column(String, ForeignKey("users.id"))

    post_id = Column(String, ForeignKey("posts.id"))
