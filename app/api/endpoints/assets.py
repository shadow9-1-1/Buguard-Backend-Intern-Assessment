from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.dependencies import get_db
from app.schemas.asset import AssetCreate, AssetResponse
from app.services.asset_service import asset_service

router = APIRouter()

@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve an asset by its ID.
    """
    return asset_service.get_asset(db=db, asset_id=asset_id)

@router.post("/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(
    *,
    db: Session = Depends(get_db),
    asset_in: AssetCreate,
):
    """
    new asset here 
    """
    return asset_service.create_asset(db=db, asset_in=asset_in)
