from fastapi import APIRouter
router=APIRouter()
DEMO_DATA_NOTICE = "synthetic-demo-data"
@router.get("/alerts")
def l(): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.get("/alerts/{alert_id}")
def g(alert_id:str): return {"alert_id":alert_id,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.post("/alerts/ingest")
def i(body:dict): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"payload":body}
@router.post("/alerts/ingest/sample")
def s(): return {"ok":True,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.patch("/alerts/{alert_id}/status")
def ps(alert_id:str,body:dict): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"payload":body}
@router.patch("/alerts/{alert_id}/assign")
def pa(alert_id:str,body:dict): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"payload":body}
@router.post("/alerts/{alert_id}/enrich")
def e(alert_id:str): return {"ioc_value":"203.0.113.10","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get("/alerts/search")
def search(q:str=""): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
