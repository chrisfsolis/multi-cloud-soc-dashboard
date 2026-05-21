import math
import os

import yaml
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.detection import DetectionRule
from app.schemas.detection import (
    DetectionRuleCreate,
    DetectionRuleResponse,
    DetectionTestRequest,
    DetectionTestResult,
)
from app.schemas.common import PaginatedResponse
from app.utils.audit_helper import create_audit_entry

router = APIRouter(tags=["detections"])

RULES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "detection_rules")


@router.get("/detections", response_model=PaginatedResponse[DetectionRuleResponse])
def list_rules(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    severity: str | None = None,
    enabled: bool | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(DetectionRule)
    if severity:
        query = query.filter(DetectionRule.severity == severity)
    if enabled is not None:
        query = query.filter(DetectionRule.enabled == enabled)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=max(1, math.ceil(total / page_size)),
    )


@router.get("/detections/{rule_id}", response_model=DetectionRuleResponse)
def get_rule(rule_id: str, db: Session = Depends(get_db)):
    rule = db.query(DetectionRule).filter(DetectionRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Detection rule not found")
    return rule


@router.post("/detections", response_model=DetectionRuleResponse, status_code=201)
def create_rule(body: DetectionRuleCreate, db: Session = Depends(get_db)):
    rule = DetectionRule(
        name=body.name,
        description=body.description,
        mitre_technique=body.mitre_technique,
        mitre_tactic=body.mitre_tactic,
        severity=body.severity,
        enabled=body.enabled,
        conditions=body.conditions,
        actions=body.actions,
    )
    if body.id:
        rule.id = body.id
    db.add(rule)
    db.commit()
    db.refresh(rule)
    create_audit_entry(db, "detection_rule", rule.id, "created")
    return rule


@router.post("/detections/test", response_model=DetectionTestResult)
def test_rule(body: DetectionTestRequest, db: Session = Depends(get_db)):
    rule = db.query(DetectionRule).filter(DetectionRule.id == body.rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Detection rule not found")

    matched = False
    matched_fields: list[str] = []
    conditions = rule.conditions or {}
    event = body.event

    title_keywords = conditions.get("alert_title_contains", [])
    event_title = str(event.get("title", "")).lower()
    for kw in title_keywords:
        if kw.lower() in event_title:
            matched = True
            matched_fields.append(f"title contains '{kw}'")

    source_cond = conditions.get("source")
    if source_cond and event.get("source") == source_cond:
        matched = True
        matched_fields.append(f"source={source_cond}")

    category_cond = conditions.get("category")
    if category_cond and event.get("category") == category_cond:
        matched = True
        matched_fields.append(f"category={category_cond}")

    indicator_keywords = conditions.get("indicator_contains", [])
    event_indicators = str(event.get("indicators", ""))
    for kw in indicator_keywords:
        if kw in event_indicators:
            matched = True
            matched_fields.append(f"indicator contains '{kw}'")

    message = "Rule matched" if matched else "Rule did not match"
    return DetectionTestResult(
        rule_id=body.rule_id,
        matched=matched,
        matched_fields=matched_fields,
        message=message,
    )


@router.post("/detections/reload", response_model=dict)
def reload_rules(db: Session = Depends(get_db)):
    if not os.path.isdir(RULES_DIR):
        raise HTTPException(status_code=404, detail="Detection rules directory not found")

    loaded = 0
    for fname in os.listdir(RULES_DIR):
        if not fname.endswith((".yml", ".yaml")):
            continue
        fpath = os.path.join(RULES_DIR, fname)
        with open(fpath) as f:
            data = yaml.safe_load(f)
        if not data:
            continue

        rule_id = data.get("id", fname.rsplit(".", 1)[0])
        existing = db.query(DetectionRule).filter(DetectionRule.id == rule_id).first()

        conditions = data.get("conditions", {})
        actions_raw = data.get("actions", [])
        actions = []
        for a in actions_raw:
            if isinstance(a, str):
                actions.append(a)
            else:
                actions.append(a)

        if existing:
            existing.name = data.get("name", existing.name)
            existing.description = data.get("description", existing.description)
            existing.mitre_technique = data.get("mitre_technique")
            existing.mitre_tactic = data.get("mitre_tactic")
            existing.severity = data.get("severity", "medium")
            existing.enabled = data.get("enabled", True)
            existing.conditions = conditions
            existing.actions = actions
        else:
            rule = DetectionRule(
                id=rule_id,
                name=data.get("name", ""),
                description=data.get("description"),
                mitre_technique=data.get("mitre_technique"),
                mitre_tactic=data.get("mitre_tactic"),
                severity=data.get("severity", "medium"),
                enabled=data.get("enabled", True),
                conditions=conditions,
                actions=actions,
            )
            db.add(rule)
        loaded += 1

    db.commit()
    return {"reloaded": True, "rules_loaded": loaded}
