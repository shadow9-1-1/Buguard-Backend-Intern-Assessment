from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset import AssetCreate

class AssetRepository:
    def create(self, db: Session, obj_in: AssetCreate) -> Asset:
        db_obj = Asset(
            type=obj_in.type,
            value=obj_in.value,
            status=obj_in.status,
            source=obj_in.source,
            tags=obj_in.tags,
            metadata=obj_in.metadata,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_type_and_value(self, db: Session, asset_type: str, value: str) -> Asset | None:
        return db.query(Asset).filter(Asset.type == asset_type, Asset.value == value).first()

asset_repo = AssetRepository()
