from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.incident import Incident, IncidentNote
from app.models.alert import Alert
from app.models.asset import Asset
from app.schemas.report import ReportResponse

router = APIRouter(tags=["reports"])


@router.get("/reports/incidents/{incident_id}", response_model=ReportResponse)
def incident_report(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    md = f"# Incident Report: {incident.id}\n\n"
    md += f"## Summary\n"
    md += f"**Title:** {incident.title}\n"
    md += f"**Severity:** {incident.severity.capitalize()} | **Status:** {incident.status.capitalize()}\n"
    if incident.assigned_to:
        md += f"**Assigned to:** {incident.assigned_to}\n"
    md += "\n"

    md += "## Correlated Alerts\n"
    md += "| Time | Source | Title | Severity |\n|------|--------|-------|----------|\n"
    for a in incident.alerts:
        ts = a.created_at.strftime("%H:%M") if a.created_at else ""
        md += f"| {ts} | {a.source} | {a.title} | {a.severity} |\n"

    asset_ids = set(a.asset_id for a in incident.alerts if a.asset_id)
    if asset_ids:
        md += "\n## Affected Assets\n"
        md += "| Asset | Provider | Risk Score |\n|-------|----------|------------|\n"
        for aid in asset_ids:
            asset = db.query(Asset).filter(Asset.id == aid).first()
            if asset:
                md += f"| {asset.name} | {asset.provider.upper()} | {asset.risk_score} |\n"

    notes = db.query(IncidentNote).filter(IncidentNote.incident_id == incident_id).all()
    if notes:
        md += "\n## Analyst Notes\n"
        for n in notes:
            md += f"> {n.content}\n> — {n.author}\n\n"

    return ReportResponse(
        format="markdown",
        generated_at=datetime.now(timezone.utc),
        markdown=md,
    )


@router.get("/reports/executive-summary", response_model=ReportResponse)
def executive_summary(db: Session = Depends(get_db)):
    total_alerts = db.query(func.count(Alert.id)).scalar() or 0
    total_incidents = db.query(func.count(Incident.id)).scalar() or 0
    open_inc = db.query(func.count(Incident.id)).filter(Incident.status.in_(["new", "investigating"])).scalar() or 0
    fp = db.query(func.count(Alert.id)).filter(Alert.status == "false_positive").scalar() or 0
    fp_rate = round(fp / total_alerts * 100, 1) if total_alerts > 0 else 0

    providers = db.query(Alert.source, func.count(Alert.id)).group_by(Alert.source).all()

    md = "# Executive Summary\n\n"
    md += "## Key Metrics\n"
    md += "| Metric | Value |\n|--------|-------|\n"
    md += f"| Total Alerts | {total_alerts} |\n"
    md += f"| Total Incidents | {total_incidents} |\n"
    md += f"| Open Incidents | {open_inc} |\n"
    md += f"| False Positive Rate | {fp_rate}% |\n\n"

    md += "## Provider Breakdown\n"
    for source, count in providers:
        pct = round(count / total_alerts * 100) if total_alerts > 0 else 0
        md += f"- {source.upper()}: {count} alerts ({pct}%)\n"

    top_assets = db.query(Asset).order_by(Asset.risk_score.desc()).limit(5).all()
    if top_assets:
        md += "\n## Top Risks\n"
        for i, a in enumerate(top_assets, 1):
            md += f"{i}. {a.name} (risk: {a.risk_score})\n"

    return ReportResponse(
        format="markdown",
        generated_at=datetime.now(timezone.utc),
        markdown=md,
    )


@router.get("/reports/monthly-soc", response_model=ReportResponse)
def monthly_soc(db: Session = Depends(get_db)):
    total_alerts = db.query(func.count(Alert.id)).scalar() or 0
    total_incidents = db.query(func.count(Incident.id)).scalar() or 0
    critical = db.query(func.count(Incident.id)).filter(Incident.severity == "critical").scalar() or 0

    severity_counts = db.query(Alert.severity, func.count(Alert.id)).group_by(Alert.severity).all()

    md = "# Monthly SOC Report\n\n"
    md += "## Overview\n"
    md += f"- **Total Alerts:** {total_alerts}\n"
    md += f"- **Total Incidents:** {total_incidents}\n"
    md += f"- **Critical Incidents:** {critical}\n\n"

    md += "## Alert Breakdown by Severity\n"
    md += "| Severity | Count |\n|----------|-------|\n"
    for sev, cnt in severity_counts:
        md += f"| {sev.capitalize()} | {cnt} |\n"

    return ReportResponse(
        format="markdown",
        generated_at=datetime.now(timezone.utc),
        markdown=md,
    )
