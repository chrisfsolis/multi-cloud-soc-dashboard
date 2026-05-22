from fastapi import APIRouter
router = APIRouter(tags=["metrics"])
DEMO_DATA_NOTICE = "synthetic-demo-data"

@router.get('/metrics/overview')
def overview(): return {"metric":"overview","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get('/metrics/mttd')
def mttd(): return {"metric":"mttd","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get('/metrics/mtta')
def mtta(): return {"metric":"mtta","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get('/metrics/mttr')
def mttr(): return {"metric":"mttr","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get('/metrics/provider-risk')
def provider_risk(): return {"metric":"provider-risk","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get('/metrics/false-positive-rate')
def fp(): return {"metric":"false-positive-rate","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get('/metrics/alert-volume')
def av(): return {"metric":"alert-volume","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get('/metrics/incident-volume')
def iv(): return {"metric":"incident-volume","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get('/metrics/mitre-breakdown')
def mb(): return {"metric":"mitre-breakdown","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
@router.get('/metrics/top-risky-assets')
def tra(): return {"metric":"top-risky-assets","synthetic_data":True,"notice":DEMO_DATA_NOTICE}
