import math
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.playbook import Playbook, PlaybookRun
from app.schemas.playbook import (
    PlaybookCreate,
    PlaybookResponse,
    PlaybookRunCreate,
    PlaybookRunResponse,
)
from app.schemas.common import PaginatedResponse
from app.utils.audit_helper import create_audit_entry

router = APIRouter(tags=["playbooks"])


@router.get("/playbooks", response_model=PaginatedResponse[PlaybookResponse])
def list_playbooks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Playbook)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=max(1, math.ceil(total / page_size)),
    )


@router.get("/playbooks/runs", response_model=PaginatedResponse[PlaybookRunResponse])
def list_runs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    playbook_id: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(PlaybookRun)
    if status:
        query = query.filter(PlaybookRun.status == status)
    if playbook_id:
        query = query.filter(PlaybookRun.playbook_id == playbook_id)
    total = query.count()
    items = query.order_by(PlaybookRun.started_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=max(1, math.ceil(total / page_size)),
    )


@router.get("/playbooks/runs/{run_id}", response_model=PlaybookRunResponse)
def get_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(PlaybookRun).filter(PlaybookRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Playbook run not found")
    return run


@router.get("/playbooks/{playbook_id}", response_model=PlaybookResponse)
def get_playbook(playbook_id: str, db: Session = Depends(get_db)):
    playbook = db.query(Playbook).filter(Playbook.id == playbook_id).first()
    if not playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")
    return playbook


@router.post("/playbooks", response_model=PlaybookResponse, status_code=201)
def create_playbook(body: PlaybookCreate, db: Session = Depends(get_db)):
    playbook = Playbook(**body.model_dump())
    db.add(playbook)
    db.commit()
    db.refresh(playbook)
    create_audit_entry(db, "playbook", playbook.id, "created")
    return playbook


@router.post("/playbooks/{playbook_id}/run", response_model=PlaybookRunResponse, status_code=201)
def run_playbook(playbook_id: str, body: PlaybookRunCreate, db: Session = Depends(get_db)):
    playbook = db.query(Playbook).filter(Playbook.id == playbook_id).first()
    if not playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")

    initial_status = "awaiting_approval" if playbook.approval_required else "running"
    run = PlaybookRun(
        playbook_id=playbook.id,
        incident_id=body.incident_id,
        status=initial_status,
        triggered_by=body.triggered_by,
        steps=playbook.steps,
    )
    db.add(run)
    playbook.run_count += 1
    playbook.last_run = datetime.now(timezone.utc)
    db.commit()
    db.refresh(run)
    create_audit_entry(db, "playbook", playbook_id, "run_started", after_state={"run_id": run.id})
    return run


@router.post("/playbooks/runs/{run_id}/approve", response_model=PlaybookRunResponse)
def approve_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(PlaybookRun).filter(PlaybookRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Playbook run not found")
    if run.status != "awaiting_approval":
        raise HTTPException(status_code=400, detail="Run is not awaiting approval")
    run.status = "running"
    db.commit()
    db.refresh(run)
    create_audit_entry(db, "playbook_run", run_id, "approved")
    return run


@router.post("/playbooks/runs/{run_id}/cancel", response_model=PlaybookRunResponse)
def cancel_run(run_id: str, db: Session = Depends(get_db)):
    run = db.query(PlaybookRun).filter(PlaybookRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Playbook run not found")
    if run.status in ("completed", "cancelled"):
        raise HTTPException(status_code=400, detail="Run already finished")
    run.status = "cancelled"
    run.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(run)
    create_audit_entry(db, "playbook_run", run_id, "cancelled")
    return run
