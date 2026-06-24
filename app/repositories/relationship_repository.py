from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import uuid

from app.models.relationship import AssetRelationship
from app.schemas.relationship import RelationshipCreate

class RelationshipRepository:
    def create(self, db: Session, obj_in: RelationshipCreate) -> AssetRelationship:
        db_obj = AssetRelationship(
            from_asset_id=obj_in.from_asset_id,
            to_asset_id=obj_in.to_asset_id,
            type=obj_in.type
        )
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            db.rollback()
            raise
        return db_obj

    def get_by_asset_id(self, db: Session, asset_id: uuid.UUID) -> dict:
        outgoing = db.query(AssetRelationship).filter(AssetRelationship.from_asset_id == asset_id).all()
        incoming = db.query(AssetRelationship).filter(AssetRelationship.to_asset_id == asset_id).all()
        return {
            "outgoing": outgoing,
            "incoming": incoming
        }
        return {
            "outgoing": outgoing,
            "incoming": incoming
        }

    def get_graph_by_asset_id(self, db: Session, asset_id: uuid.UUID) -> dict:
        from sqlalchemy.orm import joinedload
        outgoing = db.query(AssetRelationship).options(joinedload(AssetRelationship.to_asset)).filter(AssetRelationship.from_asset_id == asset_id).all()
        incoming = db.query(AssetRelationship).options(joinedload(AssetRelationship.from_asset)).filter(AssetRelationship.to_asset_id == asset_id).all()
        return {
            "outgoing": outgoing,
            "incoming": incoming
        }

    def get_specific_relationship(self, db: Session, from_id: uuid.UUID, to_id: uuid.UUID, rel_type: str) -> Optional[AssetRelationship]:
        return db.query(AssetRelationship).filter(
            AssetRelationship.from_asset_id == from_id,
            AssetRelationship.to_asset_id == to_id,
            AssetRelationship.type == rel_type
        ).first()

relationship_repo = RelationshipRepository()
