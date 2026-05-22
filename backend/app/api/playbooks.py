from fastapi import APIRouter
router=APIRouter()
DEMO_DATA_NOTICE = "synthetic-demo-data"
@router.get("/playbooks")
def l(): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.get("/playbooks/{playbook_id}")
def g(playbook_id:str): return {"id":playbook_id,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.post("/playbooks/{playbook_id}/run")
def run(playbook_id:str,body:dict): return {"status":"Waiting for Approval","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.post("/playbooks/runs/{run_id}/approve")
def ap(run_id:str,body:dict): return {"status":"Running","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.post("/playbooks/runs/{run_id}/cancel")
def ca(run_id:str): return {"status":"Cancelled","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get("/playbooks/runs")
def runs(): return {"synthetic_data":True,"notice":DEMO_DATA_NOTICE,"items":[]}
@router.get("/playbooks/runs/{run_id}")
def gr(run_id:str): return {"id":run_id,"synthetic_data":True,"notice":DEMO_DATA_NOTICE}
