from fastapi import APIRouter
from app.api.endpoints import auth, users, instagram
from app.api.v1.endpoints import instagram_auth

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(instagram.router, prefix="/instagram", tags=["Instagram"])
api_router.include_router(instagram_auth.router, prefix="/instagram/auth", tags=["Instagram OAuth"])

__all__ = ["api_router"]
