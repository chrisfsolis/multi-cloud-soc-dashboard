import json
import os
import logging

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.alert import Alert
from app.models.incident import Incident, IncidentNote, incident_alerts
from app.models.asset import Asset
from app.models.detection import DetectionRule
from app.models.playbook import Playbook, PlaybookRun
from app.models.audit import AuditEntry
from app.auth.password import hash_password

logger = logging.getLogger("soc.seed")

SYNTHETIC_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "synthetic_data")


def _load_json(filename: str) -> dict:
    path = os.path.join(SYNTHETIC_DIR, filename)
    if not os.path.exists(path):
        logger.warning("Synthetic data file not found: %s", path)
        return {}
    with open(path) as f:
        return json.load(f)


def seed_users(db: Session) -> None:
    if db.query(User).count() > 0:
        return
    users = [
        User(
            id="user-admin",
            username="admin",
            email="admin@soc.internal",
            hashed_password=hash_password("admin123"),
            role="admin",
        ),
        User(
            id="user-analyst",
            username="analyst",
            email="analyst@soc.internal",
            hashed_password=hash_password("analyst123"),
            role="analyst",
        ),
        User(
            id="user-viewer",
            username="viewer",
            email="viewer@soc.internal",
            hashed_password=hash_password("viewer123"),
            role="viewer",
        ),
    ]
    db.add_all(users)
    db.commit()
    logger.info("Seeded %d users", len(users))


def seed_assets(db: Session) -> None:
    if db.query(Asset).count() > 0:
        return
    assets = [
        Asset(id="ast-iam-deploy-bot", name="deploy-bot (IAM)", type="IAMUser", provider="aws", environment="production", owner="platform-team@company.com", criticality="high", risk_score=92),
        Asset(id="ast-vm-prod-web-03", name="prod-web-03 (EC2)", type="EC2", provider="aws", environment="production", owner="infra@company.com", criticality="high", risk_score=85),
        Asset(id="ast-az-sql-primary", name="sql-primary (Azure SQL)", type="AzureSQL", provider="azure", environment="production", owner="dba@company.com", criticality="critical", risk_score=78),
        Asset(id="ast-gcp-fw-allow-all", name="allow-all (GCP Firewall)", type="Firewall", provider="gcp", environment="production", owner="netops@company.com", criticality="high", risk_score=71),
        Asset(id="ast-az-blob-public", name="public-uploads (Blob)", type="StorageAccount", provider="azure", environment="staging", owner="dev@company.com", criticality="medium", risk_score=68),
    ]
    db.add_all(assets)
    db.commit()
    logger.info("Seeded %d assets", len(assets))


def seed_alerts(db: Session) -> None:
    if db.query(Alert).count() > 0:
        return
    data = _load_json("alerts_ingest.json")

    alerts = [
        Alert(
            id="alt-20260521-a7f3",
            source="aws",
            provider_alert_id="gd-9bc2e1f4",
            title="Unauthorized IAM access from malicious IP",
            severity="high",
            status="new",
            mitre_tactic="Initial Access",
            mitre_technique="T1078",
            asset_id="ast-iam-deploy-bot",
            ioc_values=["198.51.100.44"],
            raw_event=data.get("aws_guardduty_input", {}).get("raw"),
        ),
        Alert(
            id="alt-20260521-f8a1",
            source="azure",
            provider_alert_id="sentinel-bf-001",
            title="Brute-force attack against Azure AD",
            severity="high",
            status="new",
            mitre_tactic="Credential Access",
            mitre_technique="T1110",
            asset_id="ast-iam-deploy-bot",
            ioc_values=[],
            raw_event=data.get("azure_sentinel_input", {}).get("raw"),
        ),
        Alert(
            id="alt-20260521-c1d2",
            source="gcp",
            provider_alert_id="scc-fw-001",
            title="Open firewall rule detected - 0.0.0.0/0",
            severity="high",
            status="investigating",
            mitre_tactic="Defense Evasion",
            mitre_technique="T1562",
            asset_id="ast-gcp-fw-allow-all",
            ioc_values=["0.0.0.0/0"],
            raw_event=data.get("gcp_scc_input", {}).get("raw"),
        ),
        Alert(
            id="alt-20260521-d3e4",
            source="aws",
            provider_alert_id="gd-failed-login-2",
            title="Failed console login — deploy-bot",
            severity="medium",
            status="resolved",
            mitre_tactic="Credential Access",
            mitre_technique="T1110",
            asset_id="ast-iam-deploy-bot",
        ),
        Alert(
            id="alt-20260521-e5f6",
            source="azure",
            provider_alert_id="sentinel-blob-001",
            title="Public blob storage access detected",
            severity="medium",
            status="false_positive",
            mitre_tactic="Collection",
            mitre_technique="T1530",
            asset_id="ast-az-blob-public",
        ),
    ]
    db.add_all(alerts)
    db.commit()
    logger.info("Seeded %d alerts", len(alerts))


def seed_incidents(db: Session) -> None:
    if db.query(Incident).count() > 0:
        return
    inc = Incident(
        id="inc-20260521-001",
        title="Coordinated IAM Brute Force — deploy-bot",
        severity="critical",
        status="investigating",
        assigned_to="analyst@soc.internal",
        source_providers=["aws", "azure"],
        mitre_tactics=["Credential Access", "Initial Access"],
        detection_rule="det-001",
    )
    db.add(inc)
    db.flush()

    alert1 = db.query(Alert).filter(Alert.id == "alt-20260521-a7f3").first()
    alert2 = db.query(Alert).filter(Alert.id == "alt-20260521-f8a1").first()
    if alert1:
        db.execute(incident_alerts.insert().values(incident_id=inc.id, alert_id=alert1.id))
    if alert2:
        db.execute(incident_alerts.insert().values(incident_id=inc.id, alert_id=alert2.id))

    note = IncidentNote(
        id="note-seed-001",
        incident_id=inc.id,
        content="Confirmed malicious — escalating to IR",
        author="analyst@soc.internal",
    )
    db.add(note)
    db.commit()
    logger.info("Seeded incidents")


def seed_detection_rules(db: Session) -> None:
    if db.query(DetectionRule).count() > 0:
        return
    rules = [
        DetectionRule(
            id="det-001",
            name="Brute Force - Multi-Cloud IAM",
            description="5+ failed login alerts from same asset within 10 minutes",
            mitre_technique="T1110",
            mitre_tactic="Credential Access",
            severity="critical",
            enabled=True,
            conditions={"alert_title_contains": ["failed login", "brute-force", "sign-in failure"], "threshold": 5, "window_minutes": 10, "group_by": "asset_id"},
            actions=["create_incident", {"notify_channel": "soc-critical"}],
        ),
        DetectionRule(
            id="det-002",
            name="Open Firewall Rule - GCP",
            description="Firewall rule allows ingress from 0.0.0.0/0 on sensitive ports",
            mitre_technique="T1562",
            mitre_tactic="Defense Evasion",
            severity="high",
            enabled=True,
            conditions={"source": "gcp", "category": "OPEN_FIREWALL", "indicator_contains": ["0.0.0.0/0"]},
            actions=["create_incident", {"notify_channel": "soc-high"}],
        ),
        DetectionRule(
            id="det-003",
            name="Public Blob Storage - Azure",
            description="Blob container with anonymous public read access detected",
            mitre_technique="T1530",
            mitre_tactic="Collection",
            severity="high",
            enabled=True,
            conditions={"source": "azure", "alert_title_contains": ["public access", "anonymous", "blob"], "resource_type": "StorageAccount"},
            actions=["create_incident", {"notify_channel": "soc-high"}],
        ),
    ]
    db.add_all(rules)
    db.commit()
    logger.info("Seeded %d detection rules", len(rules))


def seed_playbooks(db: Session) -> None:
    if db.query(Playbook).count() > 0:
        return
    pb = Playbook(
        id="pb-disable-iam-key",
        name="Disable Compromised IAM Key",
        description="Isolate compromised IAM credentials across AWS accounts",
        trigger="manual | detection_rule",
        approval_required=True,
        steps=[
            {"order": 1, "action": "lookup_iam_key", "description": "Retrieve key metadata from AWS IAM"},
            {"order": 2, "action": "disable_access_key", "description": "Disable the access key", "requires_approval": True},
            {"order": 3, "action": "notify_slack", "description": "Post to #soc-incidents", "channel": "soc-incidents"},
            {"order": 4, "action": "create_jira_ticket", "description": "Open IR ticket in Jira", "project": "IR"},
        ],
        created_by="soc-lead@internal",
        run_count=14,
    )
    db.add(pb)
    db.flush()

    run = PlaybookRun(
        id="run-20260521-003",
        playbook_id=pb.id,
        incident_id="inc-20260521-001",
        status="awaiting_approval",
        triggered_by="detection_rule:det-001",
        steps=[
            {"order": 1, "action": "lookup_iam_key", "status": "completed", "output": {"key_id": "AKIAIOSFODNN7EXAMPLE", "user": "deploy-bot"}},
            {"order": 2, "action": "disable_access_key", "status": "pending_approval"},
            {"order": 3, "action": "notify_slack", "status": "pending"},
            {"order": 4, "action": "create_jira_ticket", "status": "pending"},
        ],
    )
    db.add(run)
    db.commit()
    logger.info("Seeded playbooks")


def seed_audit_entries(db: Session) -> None:
    if db.query(AuditEntry).count() > 0:
        return
    data = _load_json("audit.json")
    entries_data = data.get("entries", [])
    for e in entries_data:
        entry = AuditEntry(
            id=e.get("audit_id", None),
            entity_type=e["entity_type"],
            entity_id=e["entity_id"],
            action=e["action"],
            actor=e["actor"],
            before_state=e.get("before"),
            after_state=e.get("after"),
            ip_address=e.get("ip_address"),
        )
        db.add(entry)
    db.commit()
    logger.info("Seeded %d audit entries", len(entries_data))


def seed_all(db: Session) -> None:
    seed_users(db)
    seed_assets(db)
    seed_alerts(db)
    seed_detection_rules(db)
    seed_playbooks(db)
    seed_incidents(db)
    seed_audit_entries(db)
    logger.info("Database seeding complete")
