import uuid
from sqlalchemy.orm import Session
from app.repositories.asset_repository import asset_repo
from app.schemas.asset import AssetCreate, AssetUpdate, ImportSummary, ImportError
from fastapi import HTTPException, status
from typing import Optional, Union

class AssetService:
    def get_assets(
        self, 
        db: Session, 
        page: int, 
        size: int,
        asset_type: Optional[str] = None,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        search_value: Optional[str] = None,
        sort_by: Optional[str] = "first_seen",
        sort_order: Optional[str] = "desc",
    ):
        items, total = asset_repo.get_multi(
            db, 
            page=page, 
            size=size,
            asset_type=asset_type,
            status=status,
            tag=tag,
            search_value=search_value,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return {"items": items, "total": total, "page": page, "size": size}

    def get_asset(self, db: Session, asset_id: uuid.UUID):
        asset = asset_repo.get(db, asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        return asset

    def create_asset(self, db: Session, asset_in: AssetCreate):
        existing = asset_repo.get_by_type_and_value(db, asset_in.type, asset_in.value)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset with this type and value already exists"
            )
        return asset_repo.create(db, asset_in)

    def update_asset(self, db: Session, asset_id: uuid.UUID, asset_in: Union[AssetCreate, AssetUpdate], partial: bool = False):
        db_asset = self.get_asset(db, asset_id)
        
        update_data = asset_in.model_dump(exclude_unset=partial)
        
        if "type" in update_data or "value" in update_data:
            new_type = update_data.get("type", db_asset.type)
            new_value = update_data.get("value", db_asset.value)
            
            if new_type != db_asset.type or new_value != db_asset.value:
                existing = asset_repo.get_by_type_and_value(db, new_type, new_value)
                if existing and existing.id != asset_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Asset with this type and value already exists"
                    )
                    
        return asset_repo.update(db, db_obj=db_asset, update_data=update_data)

    def delete_asset(self, db: Session, asset_id: uuid.UUID):
        db_asset = self.get_asset(db, asset_id)
        from app.models.asset import AssetStatus
        
        if db_asset.status == AssetStatus.ARCHIVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Asset is already deleted"
            )
            
        db_asset.status = AssetStatus.ARCHIVED
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset

    def bulk_import_assets(self, db: Session, records: list) -> ImportSummary:
        total = len(records)
        imported = 0
        merged = 0
        skipped = 0
        errors = []

        for idx, raw in enumerate(records):
            try:
                asset_in = AssetCreate.model_validate(raw)
            except Exception as e:
                skipped += 1
                errors.append(ImportError(
                    index=idx,
                    record=raw,
                    reason=f"Validation error: {str(e)}"
                ))
                continue

            existing = asset_repo.get_by_type_and_value(db, asset_in.type, asset_in.value)
            if existing:
                # Merge tags, metadata, and refresh last_seen instead of skipping
                try:
                    asset_repo.merge_duplicate(db, existing, asset_in)
                    merged += 1
                except Exception as e:
                    skipped += 1
                    errors.append(ImportError(
                        index=idx,
                        record=raw,
                        reason=f"Merge error: {str(e)}"
                    ))
                continue

            try:
                asset_repo.create(db, asset_in)
                imported += 1
            except Exception as e:
                skipped += 1
                errors.append(ImportError(
                    index=idx,
                    record=raw,
                    reason=f"Database error: {str(e)}"
                ))

        return ImportSummary(
            total=total,
            imported=imported,
            merged=merged,
            skipped=skipped,
            errors=errors
        )

    def record_sighting(self, db: Session, asset_id: uuid.UUID):
        """Record a sighting: update last_seen and reactivate stale assets."""
        db_asset = self.get_asset(db, asset_id)  # raises 404 if not found
        if db_asset.status.value == "archived":
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot record a sighting for an archived asset"
            )
        return asset_repo.record_sighting(db, db_asset)

    def mark_stale(self, db: Session, asset_id: uuid.UUID):
        """Mark an asset as stale."""
        db_asset = self.get_asset(db, asset_id)
        from app.models.asset import AssetStatus
        
        if db_asset.status == AssetStatus.ARCHIVED:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot mark an archived asset as stale"
            )
            
        db_asset.status = AssetStatus.STALE
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset

asset_service = AssetService()
