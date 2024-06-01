from fastapi import APIRouter
from .auth import route_auth

api_router = APIRouter()

api_router.include_router(route_auth.router, prefix="/auth", tags=["auth"])
