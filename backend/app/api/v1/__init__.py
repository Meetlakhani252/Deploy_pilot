"""API v1 router init."""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router, prefix="/auth")

__all__ = ["api_v1_router", "auth_router"]
