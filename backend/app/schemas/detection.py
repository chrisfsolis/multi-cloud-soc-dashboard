from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DetectionRuleCreate(BaseModel):
    id: str | None = None
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    mitre_technique: str | None = None
    mitre_tactic: str | None = None
    severity: str = Field("medium", pattern="^(critical|high|medium|low)$")
    enabled: bool = True
    conditions: dict[str, Any] | None = None
    actions: list[Any] | None = None


class DetectionRuleResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    mitre_technique: str | None = None
    mitre_tactic: str | None = None
    severity: str
    enabled: bool
    conditions: Any = None
    actions: Any = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DetectionTestRequest(BaseModel):
    rule_id: str
    event: dict[str, Any]


class DetectionTestResult(BaseModel):
    rule_id: str
    matched: bool
    matched_fields: list[str] = []
    message: str = ""
