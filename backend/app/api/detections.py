from fastapi import APIRouter
router=APIRouter()
@router.get("/detections")
def l(): return []
@router.get("/detections/{rule_id}")
def g(rule_id:str): return {"id":rule_id}
@router.post("/detections/test")
def t(body:dict): return {"matched":True}
@router.post("/detections/reload")
def r(): return {"reloaded":True}
