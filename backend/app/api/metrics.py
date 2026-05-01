from fastapi import APIRouter
router = APIRouter(tags=["metrics"])

@router.get('/metrics/overview')
def overview(): return {"metric":"overview"}
@router.get('/metrics/mttd')
def mttd(): return {"metric":"mttd"}
@router.get('/metrics/mtta')
def mtta(): return {"metric":"mtta"}
@router.get('/metrics/mttr')
def mttr(): return {"metric":"mttr"}
@router.get('/metrics/provider-risk')
def provider_risk(): return {"metric":"provider-risk"}
@router.get('/metrics/false-positive-rate')
def fp(): return {"metric":"false-positive-rate"}
@router.get('/metrics/alert-volume')
def av(): return {"metric":"alert-volume"}
@router.get('/metrics/incident-volume')
def iv(): return {"metric":"incident-volume"}
@router.get('/metrics/mitre-breakdown')
def mb(): return {"metric":"mitre-breakdown"}
@router.get('/metrics/top-risky-assets')
def tra(): return {"metric":"top-risky-assets"}
