from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AlertCreate(BaseModel):
    source: str = Field(..., pattern="^(aws|azure|gcp)$")
    title: str = Field(..., min_length=1, max_length=500)
    severity: str = Field(..., pattern="^(critical|high|medium|low)$")
    provider_alert_id: str | None = None
    mitre_tactic: str | None = None
    mitre_technique: str | None = None
    asset_id: str | None = None
    ioc_values: list[str] | None = None
    raw_event: dict[str, Any] | None = None
    assigned_to: str | None = None


class AlertUpdate(BaseModel):
    status: str | None = Field(None, pattern="^(new|investigating|resolved|closed|false_positive)$")
    assigned_to: str | None = None
    severity: str | None = Field(None, pattern="^(critical|high|medium|low)$")


class AlertResponse(BaseModel):
    id: str
    source: str
    provider_alert_id: str | None = None
    title: str
    severity: str
    status: str
    mitre_tactic: str | None = None
    mitre_technique: str | None = None
    asset_id: str | None = None
    ioc_values: Any = None
    raw_event: Any = None
    assigned_to: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AlertIngest(BaseModel):
    source: str = Field(..., pattern="^(aws|azure|gcp)$")
    raw: dict[str, Any]
