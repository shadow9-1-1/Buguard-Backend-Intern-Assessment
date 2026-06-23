import uuid
import enum
from sqlalchemy import Column, String, DateTime, JSON, Enum as SQLAlchemyEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class AssetType(str, enum.Enum):
    DOMAIN = "domain"
    SUBDOMAIN = "subdomain"
    IP_ADDRESS = "ip_address"
    SERVICE = "service"
    CERTIFICATE = "certificate"
    TECHNOLOGY = "technology"

class AssetStatus(str, enum.Enum):
    ACTIVE = "active"
    STALE = "stale"
    ARCHIVED = "archived"

class Asset(Base):
    __tablename__ = 'assets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(SQLAlchemyEnum(AssetType), nullable=False, index=True)
    value = Column(String, nullable=False, index=True)
    status = Column(SQLAlchemyEnum(AssetStatus), default=AssetStatus.ACTIVE, nullable=False, index=True)
    source = Column(String, index=True)
    tags = Column(JSON, default=list)
    metadata = Column(JSON, default=dict)
    first_seen = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('type', 'value', name='_type_value_uc'),
    )

    outgoing_relationships = relationship(
        'AssetRelationship',
        foreign_keys='AssetRelationship.from_asset_id',
        back_populates='from_asset',
        cascade='all, delete-orphan'
    )
    incoming_relationships = relationship(
        'AssetRelationship',
        foreign_keys='AssetRelationship.to_asset_id',
        back_populates='to_asset',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Asset(type='{self.type}', value='{self.value}')>"
