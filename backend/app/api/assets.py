import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.asset import Asset
from app.models.alert import Alert
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse
from app.schemas.alert import AlertResponse
from app.schemas.common import PaginatedResponse
from app.utils.audit_helper import create_audit_entry

router = APIRouter(tags=["assets"])


@router.get("/assets", response_model=PaginatedResponse[AssetResponse])
def list_assets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    provider: str | None = None,
    environment: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Asset)
    if provider:
        query = query.filter(Asset.provider == provider)
    if environment:
        query = query.filter(Asset.environment == environment)
    total = query.count()
    items = query.order_by(Asset.risk_score.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=max(1, math.ceil(total / page_size)),
    )


@router.get("/assets/high-risk", response_model=list[AssetResponse])
def high_risk_assets(db: Session = Depends(get_db)):
    return db.query(Asset).filter(Asset.risk_score > 70).order_by(Asset.risk_score.desc()).all()


@router.get("/assets/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post("/assets", response_model=AssetResponse, status_code=201)
def create_asset(body: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(**body.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    create_audit_entry(db, "asset", asset.id, "created")
    return asset


@router.patch("/assets/{asset_id}", response_model=AssetResponse)
def update_asset(asset_id: str, body: AssetUpdate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    before = {"name": asset.name, "risk_score": asset.risk_score}
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(asset, key, value)
    db.commit()
    db.refresh(asset)
    create_audit_entry(db, "asset", asset_id, "updated", before_state=before, after_state=update_data)
    return asset


@router.get("/assets/{asset_id}/alerts", response_model=list[AlertResponse])
def asset_alerts(asset_id: str, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db.query(Alert).filter(Alert.asset_id == asset_id).all()


@router.get("/assets/{asset_id}/risk", response_model=dict)
def asset_risk(asset_id: str, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    alert_count = db.query(func.count(Alert.id)).filter(Alert.asset_id == asset_id).scalar() or 0
    computed_score = min(100, asset.risk_score + alert_count * 5)
    return {
        "asset_id": asset_id,
        "risk_score": asset.risk_score,
        "computed_risk_score": computed_score,
        "alert_count": alert_count,
    }
