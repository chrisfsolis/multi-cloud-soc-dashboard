# Detection Rules

The detection engine evaluates YAML-defined rules against incoming alerts. When an alert matches a rule's conditions, the specified actions are executed automatically.

## Rule Format

Detection rules are stored as YAML files in `backend/detection_rules/`. Each file defines a single rule.

### Schema

```yaml
id: <string>                    # Unique rule identifier
name: <string>                  # Human-readable rule name
description: <string>           # What the rule detects and why
mitre_technique: <string>       # MITRE ATT&CK technique ID (e.g., T1087)
mitre_tactic: <string>          # MITRE ATT&CK tactic (e.g., Discovery)
severity: <string>              # Output severity: critical | high | medium | low
enabled: <boolean>              # Whether the rule is active (default: true)

conditions:                     # Matching criteria (all must match — AND logic)
  field_name: <value>           # Exact match
  field_name:
    operator: <value>           # Operator-based match

actions:                        # List of actions to take on match
  - <action_type>
```

### Condition Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `equals` | Exact string/value match | `severity: { equals: "high" }` |
| `contains` | Substring match | `title: { contains: "brute force" }` |
| `in` | Value in list | `source: { in: ["aws", "azure"] }` |
| `regex` | Regular expression | `title: { regex: ".*lateral.*movement.*" }` |
| `gte` | Greater than or equal | `risk_score: { gte: 80 }` |
| `lte` | Less than or equal | `risk_score: { lte: 20 }` |

When a field value is specified directly (not as an object with an operator), it is treated as an `equals` match.

Multiple conditions are combined with AND logic — all conditions must match for the rule to fire.

### Action Types

| Action | Description |
|--------|-------------|
| `create_incident` | Automatically create an incident from the matching alert |
| `notify` | Send a notification to the SOC channel / assigned analyst |
| `enrich` | Trigger IOC enrichment on the alert |
| `isolate_asset` | Queue an asset isolation action (requires playbook approval) |
| `tag` | Add a tag/label to the alert |

---

## Example Rules

### Rule 1: High-Severity AWS GuardDuty Alert

Detects high or critical severity alerts from AWS GuardDuty and auto-creates incidents.

```yaml
id: rule-001
name: High Severity AWS Alert
description: >
  Triggers when a high or critical severity alert is ingested from AWS.
  Automatically creates an incident and sends a notification.
mitre_technique: T1087
mitre_tactic: Discovery
severity: high
enabled: true

conditions:
  source: aws
  severity:
    in: ["high", "critical"]

actions:
  - create_incident
  - notify
```

### Rule 2: Brute Force Login Detection

Identifies potential brute force attacks based on alert title patterns across any cloud provider.

```yaml
id: rule-002
name: Brute Force Login Attempt
description: >
  Detects alerts with titles indicating brute force or password spray attacks.
  Triggers enrichment and incident creation for investigation.
mitre_technique: T1110
mitre_tactic: Credential Access
severity: high
enabled: true

conditions:
  title:
    regex: ".*(brute.force|password.spray|failed.login.*multiple).*"
  severity:
    in: ["medium", "high", "critical"]

actions:
  - create_incident
  - enrich
  - notify
```

### Rule 3: Lateral Movement via Cross-Provider Activity

Detects potential lateral movement when activity is seen across multiple cloud environments.

```yaml
id: rule-003
name: Cross-Provider Lateral Movement
description: >
  Flags alerts related to lateral movement techniques. These often indicate
  an attacker moving between cloud environments after initial compromise.
mitre_technique: T1021
mitre_tactic: Lateral Movement
severity: critical
enabled: true

conditions:
  mitre_tactic: Lateral Movement
  severity:
    in: ["high", "critical"]

actions:
  - create_incident
  - enrich
  - isolate_asset
  - notify
```

---

## Managing Rules

### Listing Rules

```
GET /api/detections
```

Returns all loaded detection rules with their enabled/disabled status.

### Testing a Rule

```
POST /api/detections/test
```

Submit a sample event to test whether a rule would match:

```json
{
  "rule_id": "rule-001",
  "event": {
    "source": "aws",
    "severity": "high",
    "title": "Unusual API activity detected"
  }
}
```

### Reloading Rules

```
POST /api/detections/reload
```

Reloads all YAML rule files from `backend/detection_rules/` without restarting the backend. Requires admin role.

---

## Writing Custom Rules

1. Create a new `.yaml` file in `backend/detection_rules/`
2. Follow the schema above — ensure `id` and `name` are unique
3. Test the rule using the `/api/detections/test` endpoint
4. Reload rules via `/api/detections/reload` or restart the backend
5. Monitor the audit log for rule match activity
