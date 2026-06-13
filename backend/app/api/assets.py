from fastapi import APIRouter
from app.demo_data import ASSETS, envelope

router = APIRouter(tags=["assets"])


@router.get("/assets")
def list_assets():
    return envelope(ASSETS)
