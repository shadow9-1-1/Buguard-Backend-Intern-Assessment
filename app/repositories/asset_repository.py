import uuid
from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset import AssetCreate

class AssetRepository:
    def get_multi(
        self, 
        db: Session, 
        *, 
        page: int = 1, 
        size: int = 50,
        asset_type: str | None = None,
        status: str | None = None,
        tag: str | None = None,
        search_value: str | None = None,
    ) -> tuple[list[Asset], int]:
        query = db.query(Asset)
        
        if asset_type:
            query = query.filter(Asset.type == asset_type)
        if status:
            query = query.filter(Asset.status == status)
        if search_value:
            query = query.filter(Asset.value.ilike(f"%{search_value}%"))
        if tag:
            from sqlalchemy import String, cast
            query = query.filter(cast(Asset.tags, String).ilike(f'%"{tag}"%'))
            
        total = query.count()
        
        skip = (page - 1) * size
        items = query.offset(skip).limit(size).all()
        
        return items, total

    def get(self, db: Session, id: uuid.UUID) -> Asset | None:
        return db.query(Asset).filter(Asset.id == id).first()

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

    def update(self, db: Session, db_obj: Asset, update_data: dict) -> Asset:
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_type_and_value(self, db: Session, asset_type: str, value: str) -> Asset | None:
        return db.query(Asset).filter(Asset.type == asset_type, Asset.value == value).first()

asset_repo = AssetRepository()
