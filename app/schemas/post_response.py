from datetime import datetime

from pydantic import BaseModel


class MyPostResponse(BaseModel):
    id: str
    user_id: str
    content: str
    created_at: datetime
    is_anonymous: bool

    class Config:
        from_attributes = True
