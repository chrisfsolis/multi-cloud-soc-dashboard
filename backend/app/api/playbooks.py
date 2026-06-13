from fastapi import APIRouter
from app.demo_data import PLAYBOOKS, envelope

router = APIRouter(tags=["playbooks"])


@router.get("/playbooks")
def list_playbooks():
    return envelope(PLAYBOOKS)
