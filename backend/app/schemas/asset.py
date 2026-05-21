from datetime import datetime

from pydantic import BaseModel, Field


class AssetCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., min_length=1, max_length=100)
    provider: str = Field(..., pattern="^(aws|azure|gcp)$")
    environment: str = Field("production", pattern="^(production|staging|dev)$")
    owner: str | None = None
    criticality: str = Field("medium", pattern="^(critical|high|medium|low)$")
    risk_score: int = Field(0, ge=0, le=100)


class AssetUpdate(BaseModel):
    name: str | None = None
    owner: str | None = None
    environment: str | None = Field(None, pattern="^(production|staging|dev)$")
    criticality: str | None = Field(None, pattern="^(critical|high|medium|low)$")
    risk_score: int | None = Field(None, ge=0, le=100)


class AssetResponse(BaseModel):
    id: str
    name: str
    type: str
    provider: str
    environment: str
    owner: str | None = None
    criticality: str
    risk_score: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
