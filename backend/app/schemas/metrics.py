from typing import Any

from pydantic import BaseModel


class MetricsOverview(BaseModel):
    total_alerts: int = 0
    total_incidents: int = 0
    open_incidents: int = 0
    critical_incidents: int = 0
    mttd_minutes: float = 0.0
    mtta_minutes: float = 0.0
    mttr_hours: float = 0.0
    false_positive_rate: float = 0.0
    alerts_by_provider: dict[str, int] = {}
    alerts_by_severity: dict[str, int] = {}


class MTTDResponse(BaseModel):
    mttd_minutes: float = 0.0
    sample_size: int = 0


class MTTAResponse(BaseModel):
    mtta_minutes: float = 0.0
    sample_size: int = 0


class MTTRResponse(BaseModel):
    mttr_hours: float = 0.0
    sample_size: int = 0


class ProviderRisk(BaseModel):
    provider: str
    alert_count: int
    incident_count: int
    avg_risk_score: float


class MitreBreakdown(BaseModel):
    technique: str
    tactic: str | None = None
    count: int


class TopRiskyAsset(BaseModel):
    asset_id: str
    name: str
    provider: str
    risk_score: int
    open_alerts: int
