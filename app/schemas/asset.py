from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, List, Any
from pydantic import AliasChoices
from datetime import datetime
from uuid import UUID
from app.models.asset import AssetType, AssetStatus

class AssetBase(BaseModel):
    type: AssetType
    value: str
    status: Optional[AssetStatus] = AssetStatus.ACTIVE
    source: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    asset_metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        validation_alias=AliasChoices('asset_metadata', 'metadata'),
        serialization_alias="metadata"
    )

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    type: Optional[AssetType] = None
    value: Optional[str] = None
    status: Optional[AssetStatus] = None
    source: Optional[str] = None
    tags: Optional[List[str]] = None
    asset_metadata: Optional[Dict[str, Any]] = Field(
        default=None, 
        validation_alias=AliasChoices('asset_metadata', 'metadata'),
        serialization_alias="metadata"
    )

class AssetResponse(AssetBase):
    id: UUID
    first_seen: datetime
    last_seen: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class PaginatedAssetResponse(BaseModel):
    items: List[AssetResponse]
    total: int
    page: int
    size: int

class ImportError(BaseModel):
    index: int
    record: Dict[str, Any]
    reason: str

class ImportSummary(BaseModel):
    total: int
    imported: int
    merged: int
    skipped: int
    errors: List[ImportError]

class AssetImportRequest(BaseModel):
    assets: List[Dict[str, Any]]
