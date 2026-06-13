from fastapi import APIRouter
from app.demo_data import DETECTIONS, envelope

router = APIRouter(tags=["detections"])


@router.get("/detections")
def list_detections():
    return envelope(DETECTIONS)
