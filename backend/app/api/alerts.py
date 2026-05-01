from fastapi import APIRouter
router=APIRouter()
@router.get("/alerts")
def l(): return []
@router.get("/alerts/{alert_id}")
def g(alert_id:str): return {"alert_id":alert_id}
@router.post("/alerts/ingest")
def i(body:dict): return body
@router.post("/alerts/ingest/sample")
def s(): return {"ok":True}
@router.patch("/alerts/{alert_id}/status")
def ps(alert_id:str,body:dict): return body
@router.patch("/alerts/{alert_id}/assign")
def pa(alert_id:str,body:dict): return body
@router.post("/alerts/{alert_id}/enrich")
def e(alert_id:str): return {"ioc_value":"203.0.113.10"}
@router.get("/alerts/search")
def search(q:str=""): return []
