from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, List, Any
from datetime import datetime
from uuid import UUID
from app.models.asset import AssetType, AssetStatus

class AssetBase(BaseModel):
    type: AssetType
    value: str
    status: Optional[AssetStatus] = AssetStatus.ACTIVE
    source: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: UUID
    first_seen: datetime
    last_seen: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
