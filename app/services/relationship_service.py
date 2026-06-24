import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.repositories.relationship_repository import relationship_repo
from app.repositories.asset_repository import asset_repo
from app.schemas.relationship import RelationshipCreate


class RelationshipService:
    def create_relationship(self, db: Session, rel_in: RelationshipCreate):
        if rel_in.from_asset_id == rel_in.to_asset_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An asset cannot have a relationship with itself",
            )

        from_asset = asset_repo.get(db, rel_in.from_asset_id)
        if not from_asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Source asset not found"
            )

        to_asset = asset_repo.get(db, rel_in.to_asset_id)
        if not to_asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Target asset not found"
            )

        existing = relationship_repo.get_specific_relationship(
            db, rel_in.from_asset_id, rel_in.to_asset_id, rel_in.type
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Relationship already exists",
            )

        try:
            return relationship_repo.create(db, rel_in)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create relationship due to constraint violation",
            )

    def get_asset_relationships(self, db: Session, asset_id: uuid.UUID):
        asset = asset_repo.get(db, asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found"
            )

        return relationship_repo.get_by_asset_id(db, asset_id)

    def get_asset_graph(self, db: Session, asset_id: uuid.UUID) -> dict:
        asset = asset_repo.get(db, asset_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found"
            )

        graph = relationship_repo.get_graph_by_asset_id(db, asset_id)

        outgoing_formatted = [
            {"relationship_id": rel.id, "type": rel.type, "asset": rel.to_asset}
            for rel in graph["outgoing"]
        ]

        incoming_formatted = [
            {"relationship_id": rel.id, "type": rel.type, "asset": rel.from_asset}
            for rel in graph["incoming"]
        ]

        return {
            "asset": asset,
            "outgoing": outgoing_formatted,
            "incoming": incoming_formatted,
        }


relationship_service = RelationshipService()
