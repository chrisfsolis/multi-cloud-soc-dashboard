# Data Model

All models use UUID primary keys and include timestamp fields for auditing. The database is PostgreSQL 16, accessed via SQLAlchemy ORM.

## Entity Relationship Diagram

```
┌──────────┐       ┌──────────────┐       ┌─────────────┐
│   User   │       │    Alert     │       │    Asset     │
│──────────│       │──────────────│       │─────────────│
│ id (PK)  │◀──┐   │ id (PK)      │   ┌──▶│ id (PK)     │
│ username │   │   │ source       │   │   │ name        │
│ email    │   │   │ title        │   │   │ type        │
│ role     │   │   │ severity     │   │   │ provider    │
│ ...      │   │   │ asset_id(FK) │───┘   │ risk_score  │
│          │   │   │ assigned_to  │───┘   │ ...         │
│          │   │   │ ...          │       └─────────────┘
└──────────┘   │   └──────────────┘
               │
               │   ┌──────────────┐       ┌───────────────┐
               │   │   Incident   │       │ IncidentNote  │
               │   │──────────────│       │───────────────│
               │   │ id (PK)      │◀──────│ incident_id   │
               └───│ assigned_to  │       │ content       │
                   │ title        │       │ author        │
                   │ severity     │       │ ...           │
                   │ ...          │       └───────────────┘
                   └──────┬───────┘
                          │
                          │ (via PlaybookRun)
                          ▼
┌──────────────┐   ┌──────────────┐
│   Playbook   │◀──│ PlaybookRun  │
│──────────────│   │──────────────│
│ id (PK)      │   │ id (PK)      │
│ name         │   │ playbook_id  │
│ steps        │   │ incident_id  │
│ ...          │   │ status       │
└──────────────┘   │ ...          │
                   └──────────────┘

┌────────────────┐
│ DetectionRule  │
│────────────────│        ┌──────────────┐
│ id (PK)        │        │  AuditEntry  │
│ name           │        │──────────────│
│ mitre_tactic   │        │ id (PK)      │
│ conditions     │        │ entity_type  │
│ actions        │        │ entity_id    │
│ ...            │        │ action       │
└────────────────┘        │ actor        │
                          │ ...          │
                          └──────────────┘
```

---

## Models

### User

Represents a registered user of the SOC dashboard.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `username` | String | Unique, not null | Login username |
| `email` | String | Unique, not null | Email address |
| `hashed_password` | String | Not null | Bcrypt-hashed password |
| `role` | Enum | Not null, default `analyst` | One of: `admin`, `analyst`, `viewer` |
| `is_active` | Boolean | Not null, default `true` | Account active status |
| `created_at` | DateTime | Not null, auto | Account creation timestamp |

**Relationships:**
- One-to-many → Alert (via `assigned_to`)
- One-to-many → Incident (via `assigned_to`)

---

### Alert

A normalized security alert ingested from a cloud provider.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `source` | String | Not null | Cloud provider: `aws`, `azure`, `gcp` |
| `provider_alert_id` | String | Unique | Original alert ID from the provider |
| `title` | String | Not null | Alert title / summary |
| `severity` | Enum | Not null | One of: `critical`, `high`, `medium`, `low`, `informational` |
| `status` | Enum | Not null, default `new` | One of: `new`, `investigating`, `resolved`, `false_positive`, `escalated` |
| `mitre_tactic` | String | Nullable | MITRE ATT&CK tactic |
| `mitre_technique` | String | Nullable | MITRE ATT&CK technique ID |
| `asset_id` | UUID | FK → Asset.id, nullable | Associated asset |
| `ioc_values` | JSON | Nullable | Array of IOC strings (IPs, domains, hashes) |
| `raw_event` | JSON | Nullable | Original provider event payload |
| `assigned_to` | String | Nullable | Username of assigned analyst |
| `created_at` | DateTime | Not null, auto | Ingestion timestamp |
| `updated_at` | DateTime | Not null, auto-update | Last update timestamp |

**Relationships:**
- Many-to-one → Asset (via `asset_id`)
- Tracked by AuditEntry

---

### Incident

A correlated security incident, potentially spanning multiple alerts and providers.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `title` | String | Not null | Incident summary |
| `severity` | Enum | Not null | One of: `critical`, `high`, `medium`, `low` |
| `status` | Enum | Not null, default `open` | One of: `open`, `investigating`, `contained`, `resolved`, `closed` |
| `assigned_to` | String | Nullable | Username of assigned analyst |
| `source_providers` | JSON | Not null | Array of cloud providers involved |
| `mitre_tactics` | JSON | Nullable | Array of MITRE ATT&CK tactics |
| `detection_rule` | String | Nullable | ID of the detection rule that triggered this incident |
| `created_at` | DateTime | Not null, auto | Creation timestamp |
| `updated_at` | DateTime | Not null, auto-update | Last update timestamp |

**Relationships:**
- One-to-many → IncidentNote
- One-to-many → PlaybookRun
- Tracked by AuditEntry

---

### IncidentNote

A timestamped note added to an incident by an analyst.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `incident_id` | UUID | FK → Incident.id, not null | Parent incident |
| `content` | Text | Not null | Note body (Markdown supported) |
| `author` | String | Not null | Username of the note author |
| `created_at` | DateTime | Not null, auto | Note creation timestamp |

**Relationships:**
- Many-to-one → Incident (via `incident_id`)

---

### Asset

A cloud resource tracked in the asset inventory.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `name` | String | Not null | Resource name |
| `type` | String | Not null | Resource type (EC2, VM, GKE, S3, etc.) |
| `provider` | String | Not null | Cloud provider: `aws`, `azure`, `gcp` |
| `environment` | String | Not null | Deployment environment: `production`, `staging`, `development` |
| `owner` | String | Nullable | Team or individual responsible |
| `criticality` | Enum | Not null | One of: `critical`, `high`, `medium`, `low` |
| `risk_score` | Integer | Not null, default 0 | Computed risk score (0–100) |
| `created_at` | DateTime | Not null, auto | Asset discovery timestamp |
| `updated_at` | DateTime | Not null, auto-update | Last update timestamp |

**Relationships:**
- One-to-many → Alert (via `asset_id`)

---

### DetectionRule

A YAML-defined detection rule evaluated against incoming alerts.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `name` | String | Not null, unique | Rule name |
| `description` | Text | Nullable | Human-readable description |
| `mitre_technique` | String | Nullable | MITRE ATT&CK technique ID |
| `mitre_tactic` | String | Nullable | MITRE ATT&CK tactic |
| `severity` | Enum | Not null | Output severity when rule matches |
| `enabled` | Boolean | Not null, default `true` | Whether the rule is active |
| `conditions` | JSON | Not null | Rule matching conditions |
| `actions` | JSON | Not null | Actions to take on match |
| `created_at` | DateTime | Not null, auto | Rule creation timestamp |
| `updated_at` | DateTime | Not null, auto-update | Last update timestamp |

**Relationships:**
- Referenced by Incident (via `detection_rule`)

---

### Playbook

A SOAR playbook defining automated response steps.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `name` | String | Not null, unique | Playbook name |
| `description` | Text | Nullable | Purpose and scope |
| `trigger` | String | Not null | Trigger condition (manual, severity-based, rule-based) |
| `approval_required` | Boolean | Not null, default `true` | Whether admin approval is needed before execution |
| `steps` | JSON | Not null | Ordered list of step definitions |
| `created_by` | String | Not null | Username of the playbook author |
| `run_count` | Integer | Not null, default 0 | Total number of executions |
| `last_run` | DateTime | Nullable | Timestamp of last execution |
| `created_at` | DateTime | Not null, auto | Playbook creation timestamp |

**Relationships:**
- One-to-many → PlaybookRun

---

### PlaybookRun

A single execution instance of a playbook against an incident.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `playbook_id` | UUID | FK → Playbook.id, not null | Parent playbook |
| `incident_id` | UUID | FK → Incident.id, not null | Target incident |
| `status` | Enum | Not null | One of: `pending`, `awaiting_approval`, `running`, `completed`, `cancelled`, `failed` |
| `triggered_by` | String | Not null | Username who initiated the run |
| `steps` | JSON | Not null | Step execution results |
| `started_at` | DateTime | Not null, auto | Run start timestamp |
| `completed_at` | DateTime | Nullable | Run completion timestamp |

**Relationships:**
- Many-to-one → Playbook (via `playbook_id`)
- Many-to-one → Incident (via `incident_id`)

---

### AuditEntry

An immutable record of a state change for compliance and forensics.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, auto-generated | Unique identifier |
| `entity_type` | String | Not null | Type of entity: `alert`, `incident`, `asset`, `playbook`, `user` |
| `entity_id` | UUID | Not null | ID of the affected entity |
| `action` | String | Not null | Action performed: `create`, `update`, `status_change`, `assign`, `delete` |
| `actor` | String | Not null | Username who performed the action |
| `before_state` | JSON | Nullable | Entity state before the change |
| `after_state` | JSON | Nullable | Entity state after the change |
| `ip_address` | String | Nullable | Client IP address |
| `timestamp` | DateTime | Not null, auto | When the action occurred |

**Relationships:**
- References any entity via `entity_type` + `entity_id` (polymorphic)
