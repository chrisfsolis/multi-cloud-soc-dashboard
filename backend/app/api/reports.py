from fastapi import APIRouter
router=APIRouter()
DEMO_DATA_NOTICE = "synthetic-demo-data"
@router.get("/reports/incidents/{incident_id}")
def i(incident_id:str): return {"markdown":"# Incident","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get("/reports/executive-summary")
def e(): return {"markdown":"# Executive","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get("/reports/monthly-soc")
def m(): return {"markdown":"# Monthly","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
