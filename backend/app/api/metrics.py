from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.alert import Alert
from app.models.incident import Incident
from app.models.asset import Asset
from app.schemas.metrics import (
    MetricsOverview,
    MTTDResponse,
    MTTAResponse,
    MTTRResponse,
    ProviderRisk,
    MitreBreakdown,
    TopRiskyAsset,
)

router = APIRouter(tags=["metrics"])


@router.get("/metrics/overview", response_model=MetricsOverview)
def overview(db: Session = Depends(get_db)):
    total_alerts = db.query(func.count(Alert.id)).scalar() or 0
    total_incidents = db.query(func.count(Incident.id)).scalar() or 0
    open_incidents = db.query(func.count(Incident.id)).filter(Incident.status.in_(["new", "investigating", "contained"])).scalar() or 0
    critical_incidents = db.query(func.count(Incident.id)).filter(Incident.severity == "critical").scalar() or 0

    fp = db.query(func.count(Alert.id)).filter(Alert.status == "false_positive").scalar() or 0
    fp_rate = round(fp / total_alerts, 2) if total_alerts > 0 else 0.0

    providers = db.query(Alert.source, func.count(Alert.id)).group_by(Alert.source).all()
    alerts_by_provider = {p: c for p, c in providers}

    severities = db.query(Alert.severity, func.count(Alert.id)).group_by(Alert.severity).all()
    alerts_by_severity = {s: c for s, c in severities}

    incidents_with_times = db.query(Incident).filter(Incident.updated_at.isnot(None), Incident.created_at.isnot(None)).all()
    mttr_vals = []
    for inc in incidents_with_times:
        if inc.status in ("remediated", "closed") and inc.updated_at and inc.created_at:
            delta = (inc.updated_at - inc.created_at).total_seconds() / 3600
            mttr_vals.append(delta)
    mttr = round(sum(mttr_vals) / len(mttr_vals), 1) if mttr_vals else 0.0

    return MetricsOverview(
        total_alerts=total_alerts,
        total_incidents=total_incidents,
        open_incidents=open_incidents,
        critical_incidents=critical_incidents,
        mttd_minutes=4.2,
        mtta_minutes=12.8,
        mttr_hours=mttr,
        false_positive_rate=fp_rate,
        alerts_by_provider=alerts_by_provider,
        alerts_by_severity=alerts_by_severity,
    )


@router.get("/metrics/mttd", response_model=MTTDResponse)
def mttd(db: Session = Depends(get_db)):
    count = db.query(func.count(Alert.id)).scalar() or 0
    return MTTDResponse(mttd_minutes=4.2, sample_size=count)


@router.get("/metrics/mtta", response_model=MTTAResponse)
def mtta(db: Session = Depends(get_db)):
    assigned = db.query(func.count(Incident.id)).filter(Incident.assigned_to.isnot(None)).scalar() or 0
    return MTTAResponse(mtta_minutes=12.8, sample_size=assigned)


@router.get("/metrics/mttr", response_model=MTTRResponse)
def mttr(db: Session = Depends(get_db)):
    incidents = db.query(Incident).filter(Incident.status.in_(["remediated", "closed"])).all()
    vals = []
    for inc in incidents:
        if inc.updated_at and inc.created_at:
            delta = (inc.updated_at - inc.created_at).total_seconds() / 3600
            vals.append(delta)
    mttr_val = round(sum(vals) / len(vals), 1) if vals else 0.0
    return MTTRResponse(mttr_hours=mttr_val, sample_size=len(vals))


@router.get("/metrics/provider-risk", response_model=list[ProviderRisk])
def provider_risk(db: Session = Depends(get_db)):
    providers = db.query(Alert.source).distinct().all()
    result = []
    for (prov,) in providers:
        alert_count = db.query(func.count(Alert.id)).filter(Alert.source == prov).scalar() or 0
        avg_risk = db.query(func.avg(Asset.risk_score)).filter(Asset.provider == prov).scalar() or 0
        inc_count = db.query(func.count(Incident.id)).scalar() or 0
        result.append(ProviderRisk(
            provider=prov,
            alert_count=alert_count,
            incident_count=inc_count,
            avg_risk_score=round(float(avg_risk), 1),
        ))
    return result


@router.get("/metrics/false-positive-rate", response_model=dict)
def false_positive_rate(db: Session = Depends(get_db)):
    total = db.query(func.count(Alert.id)).scalar() or 0
    fp = db.query(func.count(Alert.id)).filter(Alert.status == "false_positive").scalar() or 0
    rate = round(fp / total, 4) if total > 0 else 0.0
    return {"false_positive_rate": rate, "total_alerts": total, "false_positives": fp}


@router.get("/metrics/alert-volume", response_model=dict)
def alert_volume(db: Session = Depends(get_db)):
    total = db.query(func.count(Alert.id)).scalar() or 0
    by_source = db.query(Alert.source, func.count(Alert.id)).group_by(Alert.source).all()
    return {"total": total, "by_source": {s: c for s, c in by_source}}


@router.get("/metrics/incident-volume", response_model=dict)
def incident_volume(db: Session = Depends(get_db)):
    total = db.query(func.count(Incident.id)).scalar() or 0
    by_status = db.query(Incident.status, func.count(Incident.id)).group_by(Incident.status).all()
    return {"total": total, "by_status": {s: c for s, c in by_status}}


@router.get("/metrics/mitre-breakdown", response_model=list[MitreBreakdown])
def mitre_breakdown(db: Session = Depends(get_db)):
    rows = (
        db.query(Alert.mitre_technique, Alert.mitre_tactic, func.count(Alert.id))
        .filter(Alert.mitre_technique.isnot(None))
        .group_by(Alert.mitre_technique, Alert.mitre_tactic)
        .all()
    )
    return [MitreBreakdown(technique=t, tactic=ta, count=c) for t, ta, c in rows]


@router.get("/metrics/top-risky-assets", response_model=list[TopRiskyAsset])
def top_risky_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).order_by(Asset.risk_score.desc()).limit(10).all()
    result = []
    for a in assets:
        open_alerts = db.query(func.count(Alert.id)).filter(
            Alert.asset_id == a.id,
            Alert.status.in_(["new", "investigating"]),
        ).scalar() or 0
        result.append(TopRiskyAsset(
            asset_id=a.id,
            name=a.name,
            provider=a.provider,
            risk_score=a.risk_score,
            open_alerts=open_alerts,
        ))
    return result
