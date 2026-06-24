from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.models.relationship import RelationshipType
from app.schemas.asset import AssetResponse

class RelationshipCreate(BaseModel):
    from_asset_id: UUID
    to_asset_id: UUID
    type: RelationshipType

class RelationshipResponse(BaseModel):
    id: UUID
    from_asset_id: UUID
    to_asset_id: UUID
    type: RelationshipType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AssetRelationshipsResponse(BaseModel):
    outgoing: List[RelationshipResponse]
    incoming: List[RelationshipResponse]

class RelatedAsset(BaseModel):
    relationship_id: UUID
    type: RelationshipType
    asset: AssetResponse

    model_config = ConfigDict(from_attributes=True)

class AssetGraphResponse(BaseModel):
    asset: AssetResponse
    outgoing: List[RelatedAsset]
    incoming: List[RelatedAsset]

