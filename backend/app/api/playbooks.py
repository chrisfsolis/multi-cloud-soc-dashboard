from fastapi import APIRouter
router=APIRouter()
@router.get("/playbooks")
def l(): return []
@router.get("/playbooks/{playbook_id}")
def g(playbook_id:str): return {"id":playbook_id}
@router.post("/playbooks/{playbook_id}/run")
def run(playbook_id:str,body:dict): return {"status":"Waiting for Approval"}
@router.post("/playbooks/runs/{run_id}/approve")
def ap(run_id:str,body:dict): return {"status":"Running"}
@router.post("/playbooks/runs/{run_id}/cancel")
def ca(run_id:str): return {"status":"Cancelled"}
@router.get("/playbooks/runs")
def runs(): return []
@router.get("/playbooks/runs/{run_id}")
def gr(run_id:str): return {"id":run_id}
