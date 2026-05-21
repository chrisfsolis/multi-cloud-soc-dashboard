import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.audit import AuditEntry
from app.schemas.audit import AuditEntryResponse
from app.schemas.common import PaginatedResponse

router = APIRouter(tags=["audit"])


@router.get("/audit", response_model=PaginatedResponse[AuditEntryResponse])
def list_audit(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    entity_type: str | None = None,
    action: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(AuditEntry)
    if entity_type:
        query = query.filter(AuditEntry.entity_type == entity_type)
    if action:
        query = query.filter(AuditEntry.action == action)
    total = query.count()
    items = query.order_by(AuditEntry.timestamp.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=max(1, math.ceil(total / page_size)),
    )


@router.get("/audit/{entity_type}/{entity_id}", response_model=list[AuditEntryResponse])
def entity_audit(entity_type: str, entity_id: str, db: Session = Depends(get_db)):
    return (
        db.query(AuditEntry)
        .filter(AuditEntry.entity_type == entity_type, AuditEntry.entity_id == entity_id)
        .order_by(AuditEntry.timestamp.desc())
        .all()
    )
