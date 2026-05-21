import time
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.schemas.health import HealthResponse, DependencyCheckResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        version="1.0.0",
        checked_at=datetime.now(timezone.utc),
    )


@router.get("/health/dependencies", response_model=HealthResponse)
def health_dependencies(db: Session = Depends(get_db)):
    deps: list[DependencyCheckResponse] = []

    start = time.perf_counter()
    try:
        db.execute(text("SELECT 1"))
        latency = (time.perf_counter() - start) * 1000
        deps.append(DependencyCheckResponse(name="database", status="healthy", latency_ms=round(latency, 1)))
    except Exception as exc:
        latency = (time.perf_counter() - start) * 1000
        deps.append(DependencyCheckResponse(name="database", status="unhealthy", latency_ms=round(latency, 1), error=str(exc)))

    overall = "healthy" if all(d.status == "healthy" for d in deps) else "degraded"
    return HealthResponse(
        status=overall,
        version="1.0.0",
        checked_at=datetime.now(timezone.utc),
        dependencies=deps,
    )
