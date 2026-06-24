from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.schemas.relationship import RelationshipCreate, RelationshipResponse
from app.services.relationship_service import relationship_service
from app.api.deps import get_current_user

router = APIRouter()


@router.post(
    "/", response_model=RelationshipResponse, status_code=status.HTTP_201_CREATED
)
def create_relationship(
    *,
    db: Session = Depends(get_db),
    rel_in: RelationshipCreate,
    current_user: str = Depends(get_current_user),
):
    """
    new relationship between two assets
    """
    return relationship_service.create_relationship(db=db, rel_in=rel_in)
