import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.asset import Asset, AssetStatus
from app.schemas.asset import AssetCreate
from typing import Optional


class AssetRepository:
    def get_multi(
        self,
        db: Session,
        *,
        page: int = 1,
        size: int = 50,
        asset_type: Optional[str] = None,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        search_value: Optional[str] = None,
        sort_by: Optional[str] = "first_seen",
        sort_order: Optional[str] = "desc",
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

        if hasattr(Asset, sort_by):
            sort_column = getattr(Asset, sort_by)
            if sort_order.lower() == "asc":
                query = query.order_by(sort_column.asc())
            else:
                query = query.order_by(sort_column.desc())

        total = query.count()

        skip = (page - 1) * size
        items = query.offset(skip).limit(size).all()

        return items, total

    def get(self, db: Session, id: uuid.UUID) -> Optional[Asset]:
        return db.query(Asset).filter(Asset.id == id).first()

    def create(self, db: Session, obj_in: AssetCreate) -> Asset:
        db_obj = Asset(
            type=obj_in.type,
            value=obj_in.value,
            status=obj_in.status,
            source=obj_in.source,
            tags=obj_in.tags,
            asset_metadata=obj_in.asset_metadata,
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

    def get_by_type_and_value(
        self, db: Session, asset_type: str, value: str
    ) -> Optional[Asset]:
        return (
            db.query(Asset)
            .filter(Asset.type == asset_type, Asset.value == value)
            .first()
        )

    def merge_duplicate(
        self, db: Session, db_obj: Asset, incoming: AssetCreate
    ) -> Asset:
        """Merge tags (union) and metadata (incoming overwrites), reactivate if stale, and refresh last_seen."""
        # Merge tags: union of both lists, preserving order, deduplicating
        existing_tags = list(db_obj.tags or [])
        new_tags = list(incoming.tags or [])
        merged_tags = existing_tags + [t for t in new_tags if t not in existing_tags]

        # Merge metadata: existing base, incoming values overwrite matching keys
        existing_meta = dict(db_obj.asset_metadata or {})
        new_meta = dict(incoming.asset_metadata or {})
        merged_meta = {**existing_meta, **new_meta}

        db_obj.tags = merged_tags
        db_obj.asset_metadata = merged_meta
        # Reactivate stale assets when seen again via import
        if db_obj.status == AssetStatus.STALE:
            db_obj.status = AssetStatus.ACTIVE
        # Force last_seen refresh explicitly (onupdate alone may not fire without a column change)
        db_obj.last_seen = datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def record_sighting(self, db: Session, db_obj: Asset) -> Asset:
        """Record a sighting: refresh last_seen and reactivate stale assets."""
        if db_obj.status == AssetStatus.STALE:
            db_obj.status = AssetStatus.ACTIVE
        # Explicitly set last_seen so it always updates regardless of other changes
        db_obj.last_seen = datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


asset_repo = AssetRepository()
