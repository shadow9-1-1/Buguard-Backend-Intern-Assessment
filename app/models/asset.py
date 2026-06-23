import uuid
from sqlalchemy import Column, String, DateTime, JSON, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class AssetStatus(str, enum.Enum):
    ACTIVE = "active"
    STALE = "stale"
    ARCHIVED = "archived"

class Asset(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(SQLAlchemyEnum(AssetStatus), default=AssetStatus.ACTIVE)
    tags = Column(JSON, default=[])
    metadata = Column(JSON, default={})

class Domain(Asset):
    name = Column(String, unique=True, index=True, nullable=False)

class Subdomain(Asset):
    name = Column(String, unique=True, index=True, nullable=False)

class IPAddress(Asset):
    address = Column(String, unique=True, index=True, nullable=False)

class Service(Asset):
    port = Column(String, nullable=False)
    name = Column(String)
    description = Column(String)

class Certificate(Asset):
    pass

class Technology(Asset):
    name = Column(String, index=True, nullable=False)
    version = Column(String)
    description = Column(String)
