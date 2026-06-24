from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.dependencies import get_db
from typing import Optional
from app.schemas.asset import AssetCreate, AssetResponse, AssetUpdate, PaginatedAssetResponse, AssetImportRequest, ImportSummary
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
@router.post("/import", response_model=ImportSummary, status_code=status.HTTP_200_OK)
def import_assets(
    *,
    db: Session = Depends(get_db),
    payload: AssetImportRequest,
):
    """
    Bulk import assets from a JSON dataset.
    Invalid or duplicate records are skipped and reported in the summary.
    """
    return asset_service.bulk_import_assets(db=db, records=payload.assets)

@router.post("/{asset_id}/sight", response_model=AssetResponse, status_code=status.HTTP_200_OK)
def record_sighting(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Record a sighting for an asset.
    - Updates last_seen to now.
    - Reactivates the asset if its status is stale.
    - first_seen is never modified.
    - Returns 400 if the asset is archived.
    """
    return asset_service.record_sighting(db=db, asset_id=asset_id)

@router.patch("/{asset_id}/stale", response_model=AssetResponse, status_code=status.HTTP_200_OK)
def mark_asset_stale(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Mark an asset as stale.
    - Updates status to 'stale'.
    - Returns 400 if the asset is archived.
    """
    return asset_service.mark_stale(db=db, asset_id=asset_id)

from app.schemas.relationship import AssetRelationshipsResponse
from app.services.relationship_service import relationship_service

@router.get("/{asset_id}/relationships", response_model=AssetRelationshipsResponse)
def get_asset_relationships(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve all incoming and outgoing relationships for an asset.
    """
    return relationship_service.get_asset_relationships(db=db, asset_id=asset_id)

from app.schemas.relationship import AssetGraphResponse

@router.get("/{asset_id}/graph", response_model=AssetGraphResponse)
def get_asset_graph(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Retrieve an asset and all its directly related assets.
    """
    return relationship_service.get_asset_graph(db=db, asset_id=asset_id)

