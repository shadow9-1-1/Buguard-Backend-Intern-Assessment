import uuid
import enum
from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint, CheckConstraint, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class RelationshipType(str, enum.Enum):
    RESOLVES_TO = "resolves_to"
    BELONGS_TO = "belongs_to"
    RUNS_ON = "runs_on"
    USES = "uses"
    CONNECTS_TO = "connects_to"

class AssetRelationship(Base):
    __tablename__ = 'asset_relationships'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_asset_id = Column(UUID(as_uuid=True), ForeignKey('assets.id', ondelete='CASCADE'), nullable=False, index=True)
    to_asset_id = Column(UUID(as_uuid=True), ForeignKey('assets.id', ondelete='CASCADE'), nullable=False, index=True)
    type = Column(SQLAlchemyEnum(RelationshipType), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('from_asset_id', 'to_asset_id', 'type', name='_from_to_type_uc'),
        CheckConstraint('from_asset_id != to_asset_id', name='_no_self_referencing_relationship'),
    )

    from_asset = relationship('Asset', foreign_keys=[from_asset_id], back_populates='outgoing_relationships')
    to_asset = relationship('Asset', foreign_keys=[to_asset_id], back_populates='incoming_relationships')

    def __repr__(self):
        return f"<AssetRelationship(from='{self.from_asset_id}', to='{self.to_asset_id}', type='{self.type}')>"
