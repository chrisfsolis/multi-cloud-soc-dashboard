from fastapi import APIRouter
router=APIRouter()
DEMO_DATA_NOTICE = "synthetic-demo-data"
@router.get("/audit")
def a(): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.get("/audit/{entity_type}/{entity_id}")
def e(entity_type:str,entity_id:str): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
