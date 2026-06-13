from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok", "service": "multi-cloud-soc-dashboard"}


@router.get("/health/dependencies")
def dependencies():
    return {"status": "ok", "dependencies": {"database": "not required", "cache": "not required", "cloud_credentials": "not required"}}
