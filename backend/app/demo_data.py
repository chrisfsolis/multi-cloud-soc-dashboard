from datetime import datetime, timezone

DEMO_DATA_NOTICE = "synthetic-demo-data"
NOW = datetime(2026, 6, 13, 14, 30, tzinfo=timezone.utc).isoformat()

ALERTS = [
    {
        "id": "ALRT-AWS-001",
        "title": "GuardDuty: IAM user enumerated S3 buckets from unusual ASN",
        "provider": "AWS",
        "source": "Amazon GuardDuty",
        "severity": "critical",
        "status": "open",
        "owner": "Avery Chen",
        "timestamp": "2026-06-13T13:42:00Z",
        "asset_id": "aws-iam-prod-audit-user",
        "mitre_tactic": "Discovery",
        "mitre_technique": "Cloud Service Dashboard (T1538)",
        "description": "Synthetic GuardDuty-style finding for anomalous IAM API calls and S3 ListBuckets activity.",
    },
    {
        "id": "ALRT-AZ-002",
        "title": "Sentinel: Impossible travel followed by Key Vault secret read",
        "provider": "Azure",
        "source": "Microsoft Defender for Cloud / Sentinel",
        "severity": "high",
        "status": "investigating",
        "owner": "Jordan Patel",
        "timestamp": "2026-06-13T12:58:00Z",
        "asset_id": "azure-kv-finance-prod",
        "mitre_tactic": "Credential Access",
        "mitre_technique": "Unsecured Credentials (T1552)",
        "description": "Synthetic Azure finding that links risky sign-in telemetry to Key Vault access.",
    },
    {
        "id": "ALRT-GCP-003",
        "title": "SCC: Public Cloud Storage bucket with sensitive labels",
        "provider": "GCP",
        "source": "Google Security Command Center",
        "severity": "medium",
        "status": "open",
        "owner": "Morgan Lee",
        "timestamp": "2026-06-13T11:35:00Z",
        "asset_id": "gcp-gcs-research-exports",
        "mitre_tactic": "Collection",
        "mitre_technique": "Data from Cloud Storage (T1530)",
        "description": "Synthetic SCC-style misconfiguration finding for public bucket exposure.",
    },
    {
        "id": "ALRT-AWS-004",
        "title": "CloudTrail: Security group opened to 0.0.0.0/0 on SSH",
        "provider": "AWS",
        "source": "AWS CloudTrail",
        "severity": "high",
        "status": "contained",
        "owner": "Avery Chen",
        "timestamp": "2026-06-13T10:10:00Z",
        "asset_id": "aws-ec2-bastion-prod",
        "mitre_tactic": "Initial Access",
        "mitre_technique": "External Remote Services (T1133)",
        "description": "Synthetic cloud configuration alert for broad SSH exposure.",
    },
]

INCIDENTS = [
    {
        "id": "INC-1001",
        "title": "Possible cloud credential compromise across AWS and Azure",
        "severity": "critical",
        "status": "active",
        "owner": "SOC Tier 2",
        "providers": ["AWS", "Azure"],
        "alert_ids": ["ALRT-AWS-001", "ALRT-AZ-002"],
        "created_at": "2026-06-13T14:00:00Z",
        "summary": "Correlates unusual AWS IAM discovery with Azure risky sign-in and secret access.",
    },
    {
        "id": "INC-1002",
        "title": "Cloud storage exposure review",
        "severity": "medium",
        "status": "triage",
        "owner": "Cloud Security",
        "providers": ["GCP"],
        "alert_ids": ["ALRT-GCP-003"],
        "created_at": "2026-06-13T12:05:00Z",
        "summary": "Validates public access on a labeled research export bucket and prepares remediation.",
    },
]

ASSETS = [
    {"id": "aws-iam-prod-audit-user", "name": "prod-audit-user", "provider": "AWS", "type": "IAM User", "risk_level": "critical", "region": "us-east-1", "owner": "Platform Security"},
    {"id": "azure-kv-finance-prod", "name": "kv-finance-prod", "provider": "Azure", "type": "Key Vault", "risk_level": "high", "region": "eastus", "owner": "Finance Apps"},
    {"id": "gcp-gcs-research-exports", "name": "research-exports", "provider": "GCP", "type": "Cloud Storage Bucket", "risk_level": "medium", "region": "us-central1", "owner": "Research"},
    {"id": "aws-ec2-bastion-prod", "name": "prod-bastion-01", "provider": "AWS", "type": "EC2 Instance", "risk_level": "high", "region": "us-west-2", "owner": "Infrastructure"},
]

DETECTIONS = [
    {"id": "DET-001", "name": "Cloud credential misuse correlation", "coverage": "AWS IAM, Azure AD", "mitre_tactic": "Credential Access", "enabled": True},
    {"id": "DET-002", "name": "Public storage with sensitive classification", "coverage": "AWS S3, Azure Storage, GCP GCS", "mitre_tactic": "Collection", "enabled": True},
    {"id": "DET-003", "name": "Risky administrative network change", "coverage": "CloudTrail, Azure Activity, GCP Audit Logs", "mitre_tactic": "Initial Access", "enabled": True},
]

PLAYBOOKS = [
    {"id": "PB-001", "name": "Disable suspect cloud credential", "trigger": "critical credential alert", "approval_required": True, "steps": ["Notify owner", "Disable key or user", "Open evidence task"]},
    {"id": "PB-002", "name": "Lock down public storage", "trigger": "public sensitive bucket", "approval_required": False, "steps": ["Remove public ACL", "Apply policy guardrail", "Create GRC exception review"]},
]


def envelope(items):
    return {"synthetic_data": True, "notice": DEMO_DATA_NOTICE, "items": items}


def metrics():
    severity_counts = {s: sum(1 for a in ALERTS if a["severity"] == s) for s in ["critical", "high", "medium", "low"]}
    provider_counts = {p: sum(1 for a in ALERTS if a["provider"] == p) for p in ["AWS", "Azure", "GCP"]}
    return {
        "synthetic_data": True,
        "notice": DEMO_DATA_NOTICE,
        "open_alerts": sum(1 for a in ALERTS if a["status"] in ["open", "investigating"]),
        "critical_alerts": severity_counts["critical"],
        "active_incidents": sum(1 for i in INCIDENTS if i["status"] in ["active", "triage"]),
        "cloud_assets": len(ASSETS),
        "mean_time_to_triage_minutes": 18,
        "severity_counts": severity_counts,
        "incidents_by_provider": {p: sum(1 for i in INCIDENTS if p in i["providers"]) for p in ["AWS", "Azure", "GCP"]},
        "alerts_by_provider": provider_counts,
    }
