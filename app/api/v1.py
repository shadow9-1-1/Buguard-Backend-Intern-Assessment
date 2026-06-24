from fastapi import APIRouter
from app.api.endpoints import assets

api_router = APIRouter()

api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
