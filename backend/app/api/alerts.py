from fastapi import APIRouter
from app.demo_data import ALERTS, DEMO_DATA_NOTICE, envelope

router = APIRouter(tags=["alerts"])


@router.get("/alerts")
def list_alerts():
    return envelope(ALERTS)


@router.post("/alerts/ingest")
def ingest_alert(body: dict):
    alert = {"id": f"ALRT-DEMO-{len(ALERTS) + 1:03d}", "status": "received", **body}
    return {"synthetic_data": True, "notice": DEMO_DATA_NOTICE, "message": "Demo alert accepted in memory only", "item": alert}
