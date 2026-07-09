from fastapi import FastAPI

from app.routes import follow
from app.routes.auth import router as auth_router
from app.routes.comment import router as comment_router
from app.routes.like import router as like_router
from app.routes.post import router as post_router
from app.services.google_auth import prepare_google_files
from app.routes.upload import router as upload_router
prepare_google_files()

app = FastAPI(title="Amigo API", version="1.0.0")


# Root route
@app.get("/")
def root():
    return {"message": "Deploy render running"}


# Auth routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(post_router, prefix="/posts", tags=["Posts"])
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
app.include_router(upload_router)
