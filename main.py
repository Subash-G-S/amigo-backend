from fastapi import FastAPI
from app.models.like import Like

from app.database.database import engine
from app.models.user import User
from app.routes.auth import router as auth_router
from app.models.post import Post
from app.routes.post import router as post_router
from app.routes.like import router as like_router
from app.models.comment import Comment
from app.routes.comment import router as comment_router
from app.database.database import Base
from app.models.otp import OTP
from app.models.follow import Follow
from app.routes import follow

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Amigo API",
    version="1.0.0"
)

# Root route
@app.get("/")
def root():
    return {
        "message": "Amigo Backend Running"
    }

# Auth routes
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)
app.include_router(
    post_router,
    prefix="/posts",
    tags=["Posts"]
)
app.include_router(
    like_router,
    prefix="/likes",
    tags=["Likes"],
)
app.include_router(
    comment_router,
    prefix="/comments",
    tags=["Comments"],
)
app.include_router(
    follow.router,
    prefix="/follow",
    tags=["Follow"],
)