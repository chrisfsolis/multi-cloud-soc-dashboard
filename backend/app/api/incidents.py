from fastapi import APIRouter
router=APIRouter()
@router.get("/incidents")
def l(): return []
@router.get("/incidents/{incident_id}")
def g(incident_id:str): return {"id":incident_id}
@router.post("/incidents")
def c(body:dict): return body
@router.patch("/incidents/{incident_id}/status")
def s(incident_id:str,body:dict): return body
@router.patch("/incidents/{incident_id}/assign")
def a(incident_id:str,body:dict): return body
@router.post("/incidents/{incident_id}/notes")
def n(incident_id:str,body:dict): return body
@router.get("/incidents/{incident_id}/timeline")
def t(incident_id:str): return []
@router.post("/incidents/{incident_id}/export")
def ex(incident_id:str): return {"format":"markdown"}
@router.post("/incidents/{incident_id}/run-playbook")
def rp(incident_id:str,body:dict): return body
