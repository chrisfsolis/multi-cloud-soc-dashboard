from fastapi import APIRouter
router=APIRouter()
DEMO_DATA_NOTICE = "synthetic-demo-data"
@router.get("/assets")
def l(): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.get("/assets/high-risk")
def h(): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.get("/assets/{asset_id}")
def g(asset_id:str): return {"id":asset_id,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.patch("/assets/{asset_id}")
def p(asset_id:str,body:dict): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"payload":body}
@router.get("/assets/{asset_id}/alerts")
def a(asset_id:str): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.get("/assets/{asset_id}/risk")
def r(asset_id:str): return {"risk":50,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
