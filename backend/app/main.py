from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import alerts, assets, audit, detections, health, incidents, metrics, playbooks, reports

app = FastAPI(
    title="Multi-Cloud SOC Dashboard API",
    description="Synthetic AWS, Azure, and GCP SOC data for a safe public demo.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [health.router, alerts.router, incidents.router, assets.router, detections.router, playbooks.router, metrics.router, reports.router, audit.router]:
    app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Multi-Cloud SOC Dashboard API", "docs": "/docs", "health": "/api/health"}
