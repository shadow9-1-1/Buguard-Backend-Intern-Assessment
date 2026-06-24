from fastapi import APIRouter
from app.api.endpoints import assets, relationships, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(relationships.router, prefix="/relationships", tags=["relationships"])
