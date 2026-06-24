from sqlalchemy.orm import Session
from app.repositories.asset_repository import asset_repo
from app.schemas.asset import AssetCreate
from fastapi import HTTPException, status

class AssetService:
    def create_asset(self, db: Session, asset_in: AssetCreate):
        existing = asset_repo.get_by_type_and_value(db, asset_in.type, asset_in.value)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset with this type and value already exists"
            )
        return asset_repo.create(db, asset_in)

asset_service = AssetService()
