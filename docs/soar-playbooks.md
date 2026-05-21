# SOAR Playbooks

The Security Orchestration, Automation, and Response (SOAR) system provides automated incident response through playbooks — predefined sequences of actions that execute against incidents.

## Overview

Playbooks codify your incident response procedures into repeatable, auditable workflows. They can be triggered manually by analysts or automatically by detection rules, and can optionally require admin approval before execution.

---

## Playbook Definition Format

Playbooks are stored in the database and managed via the API. Each playbook consists of metadata and an ordered list of steps.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | Yes | Unique playbook name |
| `description` | String | No | Purpose and scope of the playbook |
| `trigger` | String | Yes | How the playbook is activated (see Trigger Types) |
| `approval_required` | Boolean | Yes | Whether admin approval is needed before execution |
| `steps` | Array | Yes | Ordered list of step definitions |
| `created_by` | String | Yes | Username of the playbook author |

### Trigger Types

| Trigger | Description |
|---------|-------------|
| `manual` | Analyst manually triggers the playbook on an incident |
| `severity:critical` | Auto-triggered when a critical-severity incident is created |
| `severity:high` | Auto-triggered when a high-severity incident is created |
| `rule:<rule_id>` | Auto-triggered when a specific detection rule creates an incident |

---

## Step Types

Each step in a playbook defines an action to perform during execution.

### Available Step Types

| Step Type | Description | Example Use |
|-----------|-------------|-------------|
| `enrich` | Run IOC enrichment on alert indicators | IP reputation, domain lookup |
| `notify` | Send notification to a channel or individual | Slack alert, email to IR team |
| `isolate` | Initiate asset isolation | Quarantine compromised EC2 instance |
| `block_ip` | Add IP to blocklist | Block attacker source IP |
| `disable_user` | Disable a user account | Disable compromised credentials |
| `snapshot` | Create forensic snapshot of asset | EBS snapshot for investigation |
| `tag` | Apply tags to related resources | Tag as "under-investigation" |
| `escalate` | Escalate to senior analyst or IR team | Page on-call responder |
| `comment` | Add an automated note to the incident | Document automated actions taken |
| `webhook` | Send data to an external webhook URL | Integration with ticketing system |

### Step Definition

```json
{
  "order": 1,
  "type": "enrich",
  "name": "Enrich IOCs",
  "description": "Look up all IOC values associated with the incident alerts",
  "config": {
    "targets": ["ip", "domain", "hash"]
  }
}
```

Each step includes:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order` | Integer | Yes | Execution order (1-based) |
| `type` | String | Yes | Step type (see table above) |
| `name` | String | Yes | Human-readable step name |
| `description` | String | No | What this step does |
| `config` | Object | No | Step-type-specific configuration |

---

## Approval Flow

When `approval_required` is `true`, the playbook run enters an approval gate before execution:

```
Analyst triggers playbook
        │
        ▼
   ┌──────────┐
   │ pending   │  (run created, waiting for submission)
   └────┬──────┘
        │
        ▼
┌──────────────────┐
│ awaiting_approval │  (submitted, waiting for admin)
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐  ┌───────────┐
│approved│  │ cancelled  │  (admin rejects)
└───┬────┘  └───────────┘
    │
    ▼
┌─────────┐
│ running  │  (steps executing sequentially)
└────┬────┘
     │
┌────┴─────┐
│          │
▼          ▼
┌──────────┐  ┌────────┐
│ completed │  │ failed │  (step error)
└──────────┘  └────────┘
```

When `approval_required` is `false`, the run transitions directly from `pending` to `running`.

---

## Run Lifecycle

### Status Transitions

| Status | Description |
|--------|-------------|
| `pending` | Run created, initial state |
| `awaiting_approval` | Waiting for admin to approve or cancel |
| `running` | Steps are being executed |
| `completed` | All steps finished successfully |
| `cancelled` | Run was cancelled by admin or analyst |
| `failed` | A step encountered an error during execution |

### Run Record

Each run stores a complete execution record:

```json
{
  "id": "run-001",
  "playbook_id": "pb-001",
  "incident_id": "inc-001",
  "status": "completed",
  "triggered_by": "analyst1",
  "steps": [
    {
      "order": 1,
      "type": "enrich",
      "name": "Enrich IOCs",
      "status": "completed",
      "started_at": "2024-12-01T12:30:01Z",
      "completed_at": "2024-12-01T12:30:05Z",
      "output": { "enriched": 3 }
    },
    {
      "order": 2,
      "type": "notify",
      "name": "Alert IR Team",
      "status": "completed",
      "started_at": "2024-12-01T12:30:05Z",
      "completed_at": "2024-12-01T12:30:06Z",
      "output": { "channel": "#ir-team", "sent": true }
    }
  ],
  "started_at": "2024-12-01T12:30:00Z",
  "completed_at": "2024-12-01T12:30:06Z"
}
```

---

## Triggering a Playbook

### Manual Trigger (via API)

```http
POST /api/playbooks/{playbook_id}/run
Content-Type: application/json
Authorization: Bearer <token>

{
  "incident_id": "inc-001",
  "triggered_by": "analyst1"
}
```

### Manual Trigger (via Incident)

```http
POST /api/incidents/{incident_id}/run-playbook
Content-Type: application/json
Authorization: Bearer <token>

{
  "playbook_id": "pb-001"
}
```

### Approving a Run

```http
POST /api/playbooks/runs/{run_id}/approve
Content-Type: application/json
Authorization: Bearer <token>

{
  "approved_by": "admin"
}
```

### Cancelling a Run

```http
POST /api/playbooks/runs/{run_id}/cancel
Authorization: Bearer <token>
```

---

## Example Playbook

### Incident Response — Compromised Credentials

```json
{
  "name": "Compromised Credentials Response",
  "description": "Automated response for incidents involving compromised user credentials",
  "trigger": "manual",
  "approval_required": true,
  "steps": [
    {
      "order": 1,
      "type": "enrich",
      "name": "Enrich IOCs",
      "description": "Look up source IPs and any associated domains",
      "config": { "targets": ["ip", "domain"] }
    },
    {
      "order": 2,
      "type": "disable_user",
      "name": "Disable Compromised Account",
      "description": "Disable the affected user account pending investigation",
      "config": { "source": "incident_context" }
    },
    {
      "order": 3,
      "type": "block_ip",
      "name": "Block Attacker IP",
      "description": "Add source IP to network blocklist",
      "config": { "duration": "24h" }
    },
    {
      "order": 4,
      "type": "notify",
      "name": "Alert IR Team",
      "description": "Send notification to incident response channel",
      "config": { "channel": "#ir-team" }
    },
    {
      "order": 5,
      "type": "comment",
      "name": "Document Actions",
      "description": "Add automated response summary to the incident",
      "config": {}
    }
  ],
  "created_by": "admin"
}
```
