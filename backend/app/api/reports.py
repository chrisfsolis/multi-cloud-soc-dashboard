from fastapi import APIRouter
router=APIRouter()
@router.get("/reports/incidents/{incident_id}")
def i(incident_id:str): return {"markdown":"# Incident"}
@router.get("/reports/executive-summary")
def e(): return {"markdown":"# Executive"}
@router.get("/reports/monthly-soc")
def m(): return {"markdown":"# Monthly"}
