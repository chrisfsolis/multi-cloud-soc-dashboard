import math
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.incident import Incident, IncidentNote, incident_alerts
from app.models.alert import Alert
from app.models.asset import Asset
from app.models.audit import AuditEntry
from app.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
    IncidentNoteCreate,
    IncidentNoteResponse,
    CorrelatedAlert,
    AffectedAsset,
)
from app.schemas.common import PaginatedResponse
from app.utils.audit_helper import create_audit_entry

router = APIRouter(tags=["incidents"])


def _build_response(incident: Incident, db: Session) -> dict:
    correlated = []
    for a in incident.alerts:
        correlated.append(CorrelatedAlert(
            alert_id=a.id, source=a.source, severity=a.severity, title=a.title
        ))

    asset_ids = set()
    for a in incident.alerts:
        if a.asset_id:
            asset_ids.add(a.asset_id)
    affected = []
    for aid in asset_ids:
        asset = db.query(Asset).filter(Asset.id == aid).first()
        if asset:
            affected.append(AffectedAsset(
                asset_id=asset.id, type=asset.type, provider=asset.provider, risk_score=asset.risk_score
            ))

    return {
        "id": incident.id,
        "title": incident.title,
        "severity": incident.severity,
        "status": incident.status,
        "assigned_to": incident.assigned_to,
        "source_providers": incident.source_providers,
        "mitre_tactics": incident.mitre_tactics,
        "detection_rule": incident.detection_rule,
        "correlated_alerts": correlated,
        "affected_assets": affected,
        "created_at": incident.created_at,
        "updated_at": incident.updated_at,
    }


@router.get("/incidents", response_model=PaginatedResponse[IncidentResponse])
def list_incidents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    severity: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Incident)
    if severity:
        query = query.filter(Incident.severity == severity)
    if status:
        query = query.filter(Incident.status == status)
    total = query.count()
    items = query.order_by(Incident.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    resp_items = [_build_response(i, db) for i in items]
    return PaginatedResponse(
        items=resp_items,
        total=total,
        page=page,
        page_size=page_size,
        pages=max(1, math.ceil(total / page_size)),
    )


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return _build_response(incident, db)


@router.post("/incidents", response_model=IncidentResponse, status_code=201)
def create_incident(body: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(
        title=body.title,
        severity=body.severity,
        status=body.status,
        assigned_to=body.assigned_to,
        source_providers=body.source_providers,
        mitre_tactics=body.mitre_tactics,
        detection_rule=body.detection_rule,
    )
    db.add(incident)
    db.flush()

    if body.alert_ids:
        for aid in body.alert_ids:
            alert = db.query(Alert).filter(Alert.id == aid).first()
            if alert:
                db.execute(incident_alerts.insert().values(incident_id=incident.id, alert_id=alert.id))

    db.commit()
    db.refresh(incident)
    create_audit_entry(db, "incident", incident.id, "created")
    return _build_response(incident, db)


@router.patch("/incidents/{incident_id}/status", response_model=IncidentResponse)
def update_incident_status(incident_id: str, body: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    before = {"status": incident.status}
    if body.status:
        incident.status = body.status
    if body.severity:
        incident.severity = body.severity
    if body.title:
        incident.title = body.title
    db.commit()
    db.refresh(incident)
    create_audit_entry(db, "incident", incident_id, "status_change", before_state=before, after_state={"status": incident.status})
    return _build_response(incident, db)


@router.patch("/incidents/{incident_id}/assign", response_model=IncidentResponse)
def assign_incident(incident_id: str, body: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    before = {"assigned_to": incident.assigned_to}
    if body.assigned_to is not None:
        incident.assigned_to = body.assigned_to
    db.commit()
    db.refresh(incident)
    create_audit_entry(db, "incident", incident_id, "assignment", before_state=before, after_state={"assigned_to": incident.assigned_to})
    return _build_response(incident, db)


@router.post("/incidents/{incident_id}/notes", response_model=IncidentNoteResponse, status_code=201)
def add_note(incident_id: str, body: IncidentNoteCreate, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    note = IncidentNote(
        incident_id=incident_id,
        content=body.content,
        author=body.author,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    create_audit_entry(db, "incident", incident_id, "note_added", actor=body.author, after_state={"content": body.content})
    return note


@router.get("/incidents/{incident_id}/timeline", response_model=list[dict])
def get_timeline(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    entries = (
        db.query(AuditEntry)
        .filter(AuditEntry.entity_id == incident_id)
        .order_by(AuditEntry.timestamp.asc())
        .all()
    )
    timeline = []
    for e in entries:
        timeline.append({
            "ts": e.timestamp.isoformat() if e.timestamp else None,
            "type": e.action,
            "detail": f"{e.action}: {e.after_state}" if e.after_state else e.action,
            "actor": e.actor,
        })
    return timeline


@router.post("/incidents/{incident_id}/export", response_model=dict)
def export_incident(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    resp = _build_response(incident, db)
    notes = db.query(IncidentNote).filter(IncidentNote.incident_id == incident_id).all()

    md = f"# Incident Report: {incident.id}\n\n"
    md += f"## Summary\n"
    md += f"**Title:** {incident.title}\n"
    md += f"**Severity:** {incident.severity.capitalize()} | **Status:** {incident.status.capitalize()}\n\n"

    md += "## Correlated Alerts\n"
    md += "| Source | Title | Severity |\n|--------|-------|----------|\n"
    for a in resp.get("correlated_alerts", []):
        md += f"| {a.source} | {a.title} | {a.severity} |\n"

    md += "\n## Affected Assets\n"
    md += "| Asset | Provider | Risk Score |\n|-------|----------|------------|\n"
    for a in resp.get("affected_assets", []):
        md += f"| {a.asset_id} | {a.provider} | {a.risk_score} |\n"

    if notes:
        md += "\n## Analyst Notes\n"
        for n in notes:
            md += f"> {n.content}\n> — {n.author}, {n.created_at.isoformat() if n.created_at else ''}\n\n"

    return {"format": "markdown", "markdown": md, "generated_at": datetime.now(timezone.utc).isoformat()}


@router.post("/incidents/{incident_id}/run-playbook", response_model=dict)
def run_playbook_for_incident(incident_id: str, body: dict, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    from app.models.playbook import Playbook, PlaybookRun
    playbook_id = body.get("playbook_id")
    if not playbook_id:
        raise HTTPException(status_code=400, detail="playbook_id required")
    playbook = db.query(Playbook).filter(Playbook.id == playbook_id).first()
    if not playbook:
        raise HTTPException(status_code=404, detail="Playbook not found")

    initial_status = "awaiting_approval" if playbook.approval_required else "running"
    run = PlaybookRun(
        playbook_id=playbook.id,
        incident_id=incident_id,
        status=initial_status,
        triggered_by=body.get("triggered_by", "manual"),
        steps=playbook.steps,
    )
    db.add(run)
    playbook.run_count += 1
    playbook.last_run = datetime.now(timezone.utc)
    db.commit()
    db.refresh(run)
    create_audit_entry(db, "incident", incident_id, "playbook_triggered", after_state={"run_id": run.id, "playbook_id": playbook.id})
    return {"run_id": run.id, "status": run.status}
