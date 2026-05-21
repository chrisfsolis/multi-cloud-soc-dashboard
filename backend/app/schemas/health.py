from datetime import datetime

from pydantic import BaseModel


class DependencyCheckResponse(BaseModel):
    name: str
    status: str
    latency_ms: float | None = None
    error: str | None = None


class HealthResponse(BaseModel):
    status: str
    version: str
    checked_at: datetime
    dependencies: list[DependencyCheckResponse] = []
