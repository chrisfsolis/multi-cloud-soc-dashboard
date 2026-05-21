# Recruiter Demo Guide

This guide walks through a live demo of the Multi-Cloud SOC Dashboard, highlighting key features and capabilities. Estimated time: 10–15 minutes.

---

## Prerequisites

- Docker and Docker Compose installed
- Ports 5173 (frontend) and 8000 (backend) available
- A modern browser (Chrome, Firefox, Edge)

---

## 1. Start the Application

### Using Docker Compose (recommended)

```bash
make up
```

This builds and starts all four services (PostgreSQL, Redis, backend, frontend). Wait for all containers to be healthy:

```bash
docker compose ps
```

### Using Local Development Servers

**Terminal 1 — Backend:**

```bash
cd backend
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Frontend:**

```bash
cd frontend
npm install
npx vite --host 0.0.0.0 --port 5173
```

### Seed the Database

Load synthetic data for the demo:

```bash
make seed
```

---

## 2. Register and Login

Open the dashboard at **http://localhost:5173**.

### Default Admin Account

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

1. Navigate to the login page
2. Enter the default credentials
3. You're now logged in as an admin with full access

### Register a New User (optional)

1. Click "Register" on the login page
2. Create an analyst account:
   - Username: `demo-analyst`
   - Email: `analyst@demo.local`
   - Password: `analyst123`
   - Role: `analyst`
3. Log in with the new account

---

## 3. View the Dashboard

After logging in, the **Dashboard Overview** page displays:

- **Total Alerts** — aggregate count across all providers
- **Open Incidents** — currently active incidents
- **MTTD / MTTA / MTTR** — key SOC performance metrics
- **Alert Volume Chart** — alerts over time by provider (AWS, Azure, GCP)
- **MITRE ATT&CK Breakdown** — tactic distribution
- **Top Risky Assets** — assets with highest risk scores
- **Provider Risk Distribution** — risk by cloud provider

> **Talking point:** "This single pane of glass consolidates security telemetry from AWS GuardDuty, Azure Sentinel, and GCP Security Command Center."

---

## 4. Browse Alerts

Navigate to **Alerts** in the sidebar.

### Alert List

- View all ingested alerts with severity badges (critical/high/medium/low)
- Filter by provider, severity, status, or date range
- Full-text search across alert titles and IOC values

### Alert Detail

Click any alert to see:

- Full alert metadata and raw event payload
- MITRE ATT&CK mapping (tactic + technique)
- Associated asset information
- IOC enrichment results (IP reputation, geolocation)
- Status and assignment controls

> **Talking point:** "Each alert is normalized into a common schema regardless of source, then enriched with threat intelligence context."

---

## 5. Create an Incident from Alerts

1. Select one or more related alerts using the checkboxes
2. Click **"Create Incident"**
3. Fill in incident details:
   - Title: "Suspicious lateral movement — AWS/Azure"
   - Severity: Critical
   - Assign to: `admin`
4. The incident is created with the selected alerts correlated

### Incident Detail

- View the **incident timeline** (chronological events)
- Add **investigation notes** (Markdown supported)
- See correlated alerts and affected assets
- Track MITRE ATT&CK tactics across the incident

> **Talking point:** "Incidents correlate alerts across cloud boundaries. A single attack chain spanning AWS and Azure is tracked as one investigation."

---

## 6. Run a Playbook on an Incident

1. Open an incident detail page
2. Click **"Run Playbook"**
3. Select a playbook (e.g., "Compromised Credentials Response")
4. The playbook run enters **awaiting_approval** status
5. As admin, click **"Approve"** to start execution
6. Watch the steps execute:
   - Enrich IOCs ✓
   - Disable compromised account ✓
   - Block attacker IP ✓
   - Notify IR team ✓
   - Document actions ✓
7. Run completes with full execution log

> **Talking point:** "SOAR playbooks automate repetitive response tasks while maintaining human oversight through the approval workflow."

---

## 7. View Metrics and Reports

### SOC Metrics

Navigate to **Metrics** to see:

- **MTTD** (Mean Time to Detect) — how quickly threats are identified
- **MTTA** (Mean Time to Acknowledge) — response time after detection
- **MTTR** (Mean Time to Resolve) — total resolution time
- **False Positive Rate** — triage accuracy
- **Alert/Incident Volume Trends** — operational load over time

### Reports

Navigate to **Reports** to generate:

- **Incident Report** — detailed Markdown report for a specific incident
- **Executive Summary** — high-level risk posture for leadership
- **Monthly SOC Report** — operational metrics and trends

> **Talking point:** "SOC managers get real-time KPIs, and leadership gets audit-ready reports — all from the same platform."

---

## 8. Show the Swagger API Docs

Open **http://localhost:8000/docs** in the browser.

- Interactive API documentation (auto-generated by FastAPI)
- Try any endpoint directly from the browser
- View request/response schemas
- Demonstrate the full REST API surface

> **Talking point:** "The entire platform is API-first — every UI action maps to a documented REST endpoint, enabling integration with existing tooling."

---

## Demo Narrative Summary

| Feature | What It Shows |
|---------|--------------|
| Multi-cloud ingestion | Unified alerting from AWS, Azure, GCP |
| Alert normalization | Common schema, MITRE mapping, IOC enrichment |
| Incident correlation | Cross-provider incident management |
| SOAR playbooks | Automated response with approval gates |
| SOC metrics | MTTD/MTTA/MTTR, false positive tracking |
| Compliance reports | Executive summaries, audit-ready exports |
| API-first design | Full REST API with Swagger docs |
| RBAC | Role-based access (admin/analyst/viewer) |
