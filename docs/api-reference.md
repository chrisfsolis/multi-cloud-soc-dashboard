# API Reference

Base URL: `http://localhost:8000/api`

Interactive Swagger docs are available at [http://localhost:8000/docs](http://localhost:8000/docs) when the backend is running.

All endpoints return JSON. Authenticated endpoints require a `Bearer` token in the `Authorization` header unless otherwise noted.

---

## Health

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/health` | No | Liveness check |
| GET | `/api/health/dependencies` | No | Dependency status (Postgres, Redis) |

### GET `/api/health`

Returns the service status.

**Response** `200 OK`

```json
{
  "status": "ok"
}
```

### GET `/api/health/dependencies`

Returns connectivity status of backend dependencies.

**Response** `200 OK`

```json
{
  "postgres": "ok",
  "redis": "ok"
}
```

---

## Auth

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register` | No | Register a new user |
| POST | `/api/auth/login` | No | Obtain a JWT token |
| GET | `/api/auth/me` | Yes | Get current user profile |

### POST `/api/auth/register`

**Request Body**

```json
{
  "username": "analyst1",
  "email": "analyst1@example.com",
  "password": "securePass123",
  "role": "analyst"
}
```

**Response** `201 Created`

```json
{
  "id": "uuid",
  "username": "analyst1",
  "email": "analyst1@example.com",
  "role": "analyst",
  "is_active": true,
  "created_at": "2024-12-01T00:00:00Z"
}
```

### POST `/api/auth/login`

**Request Body**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response** `200 OK`

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

### GET `/api/auth/me`

**Response** `200 OK`

```json
{
  "id": "uuid",
  "username": "admin",
  "email": "admin@soc.local",
  "role": "admin",
  "is_active": true
}
```

---

## Alerts

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/alerts` | Yes | List all alerts (paginated, filterable) |
| GET | `/api/alerts/{alert_id}` | Yes | Get alert detail |
| POST | `/api/alerts/ingest` | Yes | Ingest a raw cloud alert |
| POST | `/api/alerts/ingest/sample` | Yes | Ingest sample/synthetic alerts |
| PATCH | `/api/alerts/{alert_id}/status` | Yes | Update alert status |
| PATCH | `/api/alerts/{alert_id}/assign` | Yes | Assign alert to analyst |
| POST | `/api/alerts/{alert_id}/enrich` | Yes | Trigger IOC enrichment |
| GET | `/api/alerts/search` | Yes | Full-text search alerts |

### GET `/api/alerts`

Query parameters: `severity`, `status`, `provider`, `page`, `page_size`

**Response** `200 OK`

```json
[
  {
    "id": "alert-001",
    "source": "aws",
    "provider_alert_id": "arn:aws:guardduty:us-east-1:123456789:detector/abc/finding/xyz",
    "title": "Unusual API activity detected",
    "severity": "high",
    "status": "new",
    "mitre_tactic": "Discovery",
    "mitre_technique": "T1087",
    "asset_id": "asset-001",
    "ioc_values": ["203.0.113.10"],
    "raw_event": {},
    "assigned_to": null,
    "created_at": "2024-12-01T10:30:00Z",
    "updated_at": "2024-12-01T10:30:00Z"
  }
]
```

### POST `/api/alerts/ingest`

Ingest a raw alert from a cloud provider.

**Request Body**

```json
{
  "source": "aws",
  "provider_alert_id": "arn:aws:guardduty:...",
  "title": "Unusual API activity detected",
  "severity": "high",
  "mitre_tactic": "Discovery",
  "mitre_technique": "T1087",
  "asset_id": "asset-001",
  "raw_event": { "detail": {} }
}
```

**Response** `200 OK` — returns the normalized alert object.

### POST `/api/alerts/ingest/sample`

Loads synthetic sample alerts from the bundled dataset.

**Response** `200 OK`

```json
{
  "ok": true
}
```

### PATCH `/api/alerts/{alert_id}/status`

**Request Body**

```json
{
  "status": "investigating"
}
```

Valid statuses: `new`, `investigating`, `resolved`, `false_positive`, `escalated`

### PATCH `/api/alerts/{alert_id}/assign`

**Request Body**

```json
{
  "assigned_to": "analyst1"
}
```

### POST `/api/alerts/{alert_id}/enrich`

Triggers IOC enrichment (IP reputation, domain lookup, hash check).

**Response** `200 OK`

```json
{
  "ioc_value": "203.0.113.10",
  "reputation": "malicious",
  "country": "CN",
  "asn": "AS4134"
}
```

### GET `/api/alerts/search`

Query parameters: `q` (search term)

**Response** `200 OK` — returns array of matching alerts.

---

## Incidents

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/incidents` | Yes | List all incidents |
| GET | `/api/incidents/{incident_id}` | Yes | Get incident detail |
| POST | `/api/incidents` | Yes | Create a new incident |
| PATCH | `/api/incidents/{incident_id}/status` | Yes | Update incident status |
| PATCH | `/api/incidents/{incident_id}/assign` | Yes | Assign incident to analyst |
| POST | `/api/incidents/{incident_id}/notes` | Yes | Add a note to an incident |
| GET | `/api/incidents/{incident_id}/timeline` | Yes | Get incident timeline |
| POST | `/api/incidents/{incident_id}/export` | Yes | Export incident report |
| POST | `/api/incidents/{incident_id}/run-playbook` | Yes | Trigger a playbook on the incident |

### POST `/api/incidents`

**Request Body**

```json
{
  "title": "Suspicious lateral movement detected",
  "severity": "critical",
  "status": "open",
  "assigned_to": "analyst1",
  "source_providers": ["aws", "azure"],
  "mitre_tactics": ["Lateral Movement", "Credential Access"],
  "alert_ids": ["alert-001", "alert-002"]
}
```

**Response** `200 OK`

```json
{
  "id": "inc-001",
  "title": "Suspicious lateral movement detected",
  "severity": "critical",
  "status": "open",
  "assigned_to": "analyst1",
  "source_providers": ["aws", "azure"],
  "mitre_tactics": ["Lateral Movement", "Credential Access"],
  "detection_rule": null,
  "created_at": "2024-12-01T12:00:00Z",
  "updated_at": "2024-12-01T12:00:00Z"
}
```

### POST `/api/incidents/{incident_id}/notes`

**Request Body**

```json
{
  "content": "Confirmed malicious IP. Escalating to IR team.",
  "author": "analyst1"
}
```

### GET `/api/incidents/{incident_id}/timeline`

Returns an ordered list of events (status changes, notes, playbook runs) for the incident.

**Response** `200 OK`

```json
[
  {
    "timestamp": "2024-12-01T12:00:00Z",
    "event": "Incident created",
    "actor": "admin"
  },
  {
    "timestamp": "2024-12-01T12:15:00Z",
    "event": "Note added",
    "actor": "analyst1"
  }
]
```

### POST `/api/incidents/{incident_id}/export`

Exports the incident as a Markdown report.

**Response** `200 OK`

```json
{
  "format": "markdown",
  "content": "# Incident Report\n..."
}
```

### POST `/api/incidents/{incident_id}/run-playbook`

**Request Body**

```json
{
  "playbook_id": "pb-001"
}
```

---

## Assets

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/assets` | Yes | List all assets |
| GET | `/api/assets/high-risk` | Yes | List high-risk assets |
| GET | `/api/assets/{asset_id}` | Yes | Get asset detail |
| PATCH | `/api/assets/{asset_id}` | Yes | Update asset metadata |
| GET | `/api/assets/{asset_id}/alerts` | Yes | Get alerts for an asset |
| GET | `/api/assets/{asset_id}/risk` | Yes | Get risk score for an asset |

### GET `/api/assets`

**Response** `200 OK`

```json
[
  {
    "id": "asset-001",
    "name": "prod-web-server-01",
    "type": "EC2",
    "provider": "aws",
    "environment": "production",
    "owner": "platform-team",
    "criticality": "high",
    "risk_score": 85,
    "created_at": "2024-11-15T00:00:00Z",
    "updated_at": "2024-12-01T10:00:00Z"
  }
]
```

### GET `/api/assets/{asset_id}/risk`

**Response** `200 OK`

```json
{
  "risk_score": 85,
  "factors": [
    "high_severity_alerts",
    "internet_facing",
    "production_environment"
  ]
}
```

---

## Detections

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/detections` | Yes | List all detection rules |
| GET | `/api/detections/{rule_id}` | Yes | Get rule detail |
| POST | `/api/detections/test` | Yes | Test a rule against sample data |
| POST | `/api/detections/reload` | Yes (admin) | Reload rules from YAML files |

### POST `/api/detections/test`

**Request Body**

```json
{
  "rule_id": "rule-001",
  "event": {
    "source": "aws",
    "severity": "high",
    "title": "Unusual API activity"
  }
}
```

**Response** `200 OK`

```json
{
  "matched": true,
  "rule_id": "rule-001",
  "rule_name": "High Severity AWS Alert",
  "actions": ["create_incident", "notify"]
}
```

---

## Playbooks

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/playbooks` | Yes | List all playbooks |
| GET | `/api/playbooks/{playbook_id}` | Yes | Get playbook detail |
| POST | `/api/playbooks/{playbook_id}/run` | Yes | Start a playbook run |
| POST | `/api/playbooks/runs/{run_id}/approve` | Yes (admin) | Approve a pending run |
| POST | `/api/playbooks/runs/{run_id}/cancel` | Yes | Cancel a run |
| GET | `/api/playbooks/runs` | Yes | List all playbook runs |
| GET | `/api/playbooks/runs/{run_id}` | Yes | Get run detail |

### POST `/api/playbooks/{playbook_id}/run`

**Request Body**

```json
{
  "incident_id": "inc-001",
  "triggered_by": "analyst1"
}
```

**Response** `200 OK`

```json
{
  "id": "run-001",
  "playbook_id": "pb-001",
  "incident_id": "inc-001",
  "status": "awaiting_approval",
  "triggered_by": "analyst1",
  "steps": [],
  "started_at": "2024-12-01T12:30:00Z",
  "completed_at": null
}
```

### POST `/api/playbooks/runs/{run_id}/approve`

**Request Body**

```json
{
  "approved_by": "admin"
}
```

---

## Metrics

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/metrics/overview` | Yes | Dashboard overview stats |
| GET | `/api/metrics/mttd` | Yes | Mean Time to Detect |
| GET | `/api/metrics/mtta` | Yes | Mean Time to Acknowledge |
| GET | `/api/metrics/mttr` | Yes | Mean Time to Resolve |
| GET | `/api/metrics/provider-risk` | Yes | Risk breakdown by cloud provider |
| GET | `/api/metrics/false-positive-rate` | Yes | False positive rate |
| GET | `/api/metrics/alert-volume` | Yes | Alert volume over time |
| GET | `/api/metrics/incident-volume` | Yes | Incident volume over time |
| GET | `/api/metrics/mitre-breakdown` | Yes | Alert/incident breakdown by MITRE ATT&CK |
| GET | `/api/metrics/top-risky-assets` | Yes | Top assets by risk score |

### GET `/api/metrics/overview`

**Response** `200 OK`

```json
{
  "total_alerts": 247,
  "open_incidents": 12,
  "active_playbooks": 3,
  "high_risk_assets": 8,
  "mttd_minutes": 4.2,
  "mttr_hours": 2.1,
  "false_positive_rate": 0.15
}
```

### GET `/api/metrics/alert-volume`

Query parameters: `days` (default 30)

**Response** `200 OK`

```json
{
  "labels": ["2024-12-01", "2024-12-02", "2024-12-03"],
  "datasets": {
    "aws": [12, 8, 15],
    "azure": [5, 3, 7],
    "gcp": [2, 4, 1]
  }
}
```

---

## Reports

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/reports/incidents/{incident_id}` | Yes | Incident report (Markdown) |
| GET | `/api/reports/executive-summary` | Yes | Executive summary report |
| GET | `/api/reports/monthly-soc` | Yes | Monthly SOC operations report |

### GET `/api/reports/executive-summary`

**Response** `200 OK`

```json
{
  "markdown": "# Executive Summary\n\n## Key Metrics\n- Total alerts: 247\n- Open incidents: 12\n- MTTD: 4.2 min\n- MTTR: 2.1 hrs\n\n## Risk Posture\n..."
}
```

---

## Audit

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/audit` | Yes (admin) | List all audit entries |
| GET | `/api/audit/{entity_type}/{entity_id}` | Yes (admin) | Get audit trail for an entity |

### GET `/api/audit`

Query parameters: `entity_type`, `actor`, `action`, `page`, `page_size`

**Response** `200 OK`

```json
[
  {
    "id": "audit-001",
    "entity_type": "incident",
    "entity_id": "inc-001",
    "action": "status_change",
    "actor": "analyst1",
    "before_state": { "status": "open" },
    "after_state": { "status": "investigating" },
    "ip_address": "10.0.1.50",
    "timestamp": "2024-12-01T12:10:00Z"
  }
]
```

### GET `/api/audit/{entity_type}/{entity_id}`

Returns the full audit trail for a specific entity (alert, incident, asset, playbook, etc.).

**Response** `200 OK` — returns array of audit entries filtered to the entity.
