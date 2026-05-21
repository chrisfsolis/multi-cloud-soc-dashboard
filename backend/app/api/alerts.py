import json
import math
import os
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertUpdate, AlertResponse, AlertIngest
from app.schemas.common import PaginatedResponse
from app.utils.audit_helper import create_audit_entry
from app.middleware.rate_limit import limiter

router = APIRouter(tags=["alerts"])


def _normalize_alert(source: str, raw: dict[str, Any]) -> dict:
    if source == "aws":
        detail = raw.get("detail", {})
        return {
            "source": "aws",
            "provider_alert_id": f"gd-{id(raw) % 0xFFFFFF:06x}",
            "title": detail.get("type", "AWS GuardDuty Finding"),
            "severity": _map_aws_severity(detail.get("severity", 0)),
            "mitre_tactic": "Initial Access",
            "mitre_technique": "T1078",
            "raw_event": raw,
        }
    elif source == "azure":
        props = raw.get("properties", {})
        return {
            "source": "azure",
            "provider_alert_id": f"sentinel-{id(raw) % 0xFFFFFF:06x}",
            "title": props.get("alertDisplayName", "Azure Sentinel Alert"),
            "severity": (props.get("severity", "medium")).lower(),
            "mitre_tactic": (props.get("tactics", [None]) or [None])[0] or "Unknown",
            "mitre_technique": None,
            "raw_event": raw,
        }
    elif source == "gcp":
        finding = raw.get("finding", {})
        return {
            "source": "gcp",
            "provider_alert_id": f"scc-{id(raw) % 0xFFFFFF:06x}",
            "title": finding.get("category", "GCP SCC Finding"),
            "severity": (finding.get("severity", "MEDIUM")).lower(),
            "mitre_tactic": "Defense Evasion",
            "mitre_technique": "T1562",
            "raw_event": raw,
        }
    return {"source": source, "title": "Unknown alert", "severity": "low", "raw_event": raw}


def _map_aws_severity(sev: float) -> str:
    if sev >= 7:
        return "high"
    if sev >= 4:
        return "medium"
    return "low"


@router.get("/alerts/search", response_model=list[AlertResponse])
def search_alerts(
    q: str = Query("", description="Search query"),
    db: Session = Depends(get_db),
):
    if not q:
        return []
    query = db.query(Alert).filter(Alert.title.ilike(f"%{q}%"))
    return query.limit(50).all()


@router.get("/alerts", response_model=PaginatedResponse[AlertResponse])
def list_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    severity: str | None = None,
    status: str | None = None,
    source: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Alert)
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    if source:
        query = query.filter(Alert.source == source)
    total = query.count()
    items = query.order_by(Alert.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=max(1, math.ceil(total / page_size)),
    )


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/alerts/ingest", response_model=AlertResponse, status_code=201)
@limiter.limit("100/minute")
def ingest_alert(body: AlertIngest, request: Request, db: Session = Depends(get_db)):
    normalized = _normalize_alert(body.source, body.raw)
    alert = Alert(**normalized)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    create_audit_entry(db, "alert", alert.id, "created", actor="system:ingest")
    return alert


@router.post("/alerts/ingest/sample", response_model=dict)
def ingest_sample(db: Session = Depends(get_db)):
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "synthetic_data", "alerts_ingest.json")
    if not os.path.exists(data_path):
        raise HTTPException(status_code=404, detail="Sample data file not found")
    with open(data_path) as f:
        data = json.load(f)

    count = 0
    for key in ["aws_guardduty_input", "azure_sentinel_input", "gcp_scc_input"]:
        entry = data.get(key)
        if entry:
            normalized = _normalize_alert(entry["source"], entry["raw"])
            alert = Alert(**normalized)
            db.add(alert)
            count += 1
    db.commit()
    return {"ingested": count}


@router.patch("/alerts/{alert_id}/status", response_model=AlertResponse)
def update_alert_status(alert_id: str, body: AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    before = {"status": alert.status}
    if body.status:
        alert.status = body.status
    if body.severity:
        alert.severity = body.severity
    db.commit()
    db.refresh(alert)
    create_audit_entry(db, "alert", alert_id, "status_change", before_state=before, after_state={"status": alert.status})
    return alert


@router.patch("/alerts/{alert_id}/assign", response_model=AlertResponse)
def assign_alert(alert_id: str, body: AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    before = {"assigned_to": alert.assigned_to}
    if body.assigned_to is not None:
        alert.assigned_to = body.assigned_to
    db.commit()
    db.refresh(alert)
    create_audit_entry(db, "alert", alert_id, "assignment", before_state=before, after_state={"assigned_to": alert.assigned_to})
    return alert


@router.post("/alerts/{alert_id}/enrich", response_model=dict)
def enrich_alert(alert_id: str, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    enrichment_path = os.path.join(os.path.dirname(__file__), "..", "..", "synthetic_data", "enrichment.json")
    enrichment = {}
    if os.path.exists(enrichment_path):
        with open(enrichment_path) as f:
            enrichment = json.load(f)
    return {
        "alert_id": alert_id,
        "enrichments": enrichment.get("enrichments", {}),
        "enriched_at": enrichment.get("enriched_at", None),
    }
