from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PlaybookCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    trigger: str | None = None
    approval_required: bool = False
    steps: list[dict[str, Any]] | None = None
    created_by: str | None = None


class PlaybookResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    trigger: str | None = None
    approval_required: bool
    steps: Any = None
    created_by: str | None = None
    run_count: int
    last_run: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PlaybookRunCreate(BaseModel):
    incident_id: str | None = None
    triggered_by: str | None = None


class PlaybookRunResponse(BaseModel):
    id: str
    playbook_id: str
    incident_id: str | None = None
    status: str
    triggered_by: str | None = None
    steps: Any = None
    started_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}
