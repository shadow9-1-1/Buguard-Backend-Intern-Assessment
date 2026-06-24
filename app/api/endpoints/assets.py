from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.dependencies import get_db
from typing import Optional
from app.schemas.asset import AssetCreate, AssetResponse, AssetUpdate, PaginatedAssetResponse
from app.models.asset import AssetType, AssetStatus
from app.services.asset_service import asset_service

router = APIRouter()

@router.get("/", response_model=PaginatedAssetResponse)
def list_assets(
    db: Session = Depends(get_db),
    page: int = 1,
    size: int = 50,
    asset_type: Optional[AssetType] = None,
    status: Optional[AssetStatus] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "first_seen",
    sort_order: Optional[str] = "desc",
):
    """
    List assets with filtering, sorting, and pagination.
    """
    return asset_service.get_assets(
        db=db,
        page=page,
        size=size,
        asset_type=asset_type,
        status=status,
        tag=tag,
        search_value=search,
        sort_by=sort_by,
        sort_order=sort_order
    )

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

@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: UUID,
    asset_in: AssetCreate,
    db: Session = Depends(get_db),
):
    """
    Update an asset completely.
    """
    return asset_service.update_asset(db=db, asset_id=asset_id, asset_in=asset_in, partial=False)

@router.patch("/{asset_id}", response_model=AssetResponse)
def partially_update_asset(
    asset_id: UUID,
    asset_in: AssetUpdate,
    db: Session = Depends(get_db),
):
    """
    Partially update an asset.
    """
    return asset_service.update_asset(db=db, asset_id=asset_id, asset_in=asset_in, partial=True)

@router.delete("/{asset_id}", response_model=AssetResponse)
def delete_asset(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Delete an asset (soft delete).
    """
    return asset_service.delete_asset(db=db, asset_id=asset_id)
