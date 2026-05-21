import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.database import engine, SessionLocal
from app.models import Base
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.rate_limit import limiter
from app.utils.seed_data import seed_all

from app.api import alerts, incidents, assets, detections, playbooks, metrics, reports, audit, health
from app.api.auth import router as auth_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("soc")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Multi-Cloud SOC Dashboard API",
    version="1.0.0",
    description="Advanced multi-cloud SOC dashboard API combining AWS, Azure, and GCP alert ingestion with SIEM-style detection, incident correlation, SOAR playbooks, SOC metrics, and audit-ready reporting.",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(auth_router, prefix="/api")
for r in [
    alerts.router,
    incidents.router,
    assets.router,
    detections.router,
    playbooks.router,
    metrics.router,
    reports.router,
    audit.router,
    health.router,
]:
    app.include_router(r, prefix="/api")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(status_code=404, content={"detail": "Not found"})


@app.exception_handler(422)
async def validation_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": str(exc)},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.error("Internal server error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
