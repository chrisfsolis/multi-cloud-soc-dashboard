from fastapi import APIRouter
from app.demo_data import metrics

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
def dashboard_metrics():
    return metrics()


@router.get("/metrics/overview")
def overview():
    return metrics()
