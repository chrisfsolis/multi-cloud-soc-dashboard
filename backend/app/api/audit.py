from fastapi import APIRouter
router=APIRouter()
@router.get("/audit")
def a(): return []
@router.get("/audit/{entity_type}/{entity_id}")
def e(entity_type:str,entity_id:str): return []
