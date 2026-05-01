from fastapi import APIRouter
router=APIRouter()
@router.get("/health")
def h(): return {"status":"ok"}
@router.get("/health/dependencies")
def d(): return {"deps":"ok"}
