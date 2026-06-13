from fastapi import APIRouter
from app.demo_data import INCIDENTS, envelope

router = APIRouter(tags=["incidents"])


@router.get("/incidents")
def list_incidents():
    return envelope(INCIDENTS)
