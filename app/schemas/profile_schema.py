from pydantic import BaseModel

class UpdateProfile(BaseModel):
    name: str
    bio: str