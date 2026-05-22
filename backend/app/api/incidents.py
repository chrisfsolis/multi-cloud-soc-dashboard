from fastapi import APIRouter
router=APIRouter()
DEMO_DATA_NOTICE = "synthetic-demo-data"
@router.get("/incidents")
def l(): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.get("/incidents/{incident_id}")
def g(incident_id:str): return {"id":incident_id,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.post("/incidents")
def c(body:dict): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"payload":body}
@router.patch("/incidents/{incident_id}/status")
def s(incident_id:str,body:dict): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"payload":body}
@router.patch("/incidents/{incident_id}/assign")
def a(incident_id:str,body:dict): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"payload":body}
@router.post("/incidents/{incident_id}/notes")
def n(incident_id:str,body:dict): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"payload":body}
@router.get("/incidents/{incident_id}/timeline")
def t(incident_id:str): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.post("/incidents/{incident_id}/export")
def ex(incident_id:str): return {"format":"markdown","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.post("/incidents/{incident_id}/run-playbook")
def rp(incident_id:str,body:dict): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"payload":body}
