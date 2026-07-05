from pydantic import BaseModel


class CreateComment(BaseModel):
    content: str
