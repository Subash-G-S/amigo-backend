from pydantic import BaseModel


class CreatePost(BaseModel):
    content: str
    is_anonymous: bool = False
