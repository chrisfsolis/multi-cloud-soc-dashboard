from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    severity: str = Field(..., pattern="^(critical|high|medium|low)$")
    status: str = Field("new", pattern="^(new|investigating|contained|remediated|closed)$")
    assigned_to: str | None = None
    source_providers: list[str] | None = None
    mitre_tactics: list[str] | None = None
    detection_rule: str | None = None
    alert_ids: list[str] | None = None


class IncidentUpdate(BaseModel):
    title: str | None = None
    severity: str | None = Field(None, pattern="^(critical|high|medium|low)$")
    status: str | None = Field(None, pattern="^(new|investigating|contained|remediated|closed)$")
    assigned_to: str | None = None


class IncidentNoteCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)
    author: str = Field(..., min_length=1)


class IncidentNoteResponse(BaseModel):
    id: str
    incident_id: str
    content: str
    author: str
    created_at: datetime

    model_config = {"from_attributes": True}


class CorrelatedAlert(BaseModel):
    alert_id: str
    source: str
    severity: str
    title: str


class AffectedAsset(BaseModel):
    asset_id: str
    type: str
    provider: str
    risk_score: int


class IncidentResponse(BaseModel):
    id: str
    title: str
    severity: str
    status: str
    assigned_to: str | None = None
    source_providers: Any = None
    mitre_tactics: Any = None
    detection_rule: str | None = None
    correlated_alerts: list[CorrelatedAlert] = []
    affected_assets: list[AffectedAsset] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
