from fastapi import APIRouter
router=APIRouter()
DEMO_DATA_NOTICE = "synthetic-demo-data"
@router.get("/detections")
def l(): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.get("/detections/{rule_id}")
def g(rule_id:str): return {"id":rule_id,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.post("/detections/test")
def t(body:dict): return {"matched":True,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.post("/detections/reload")
def r(): return {"reloaded":True,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
