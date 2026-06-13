# Multi-Cloud SOC Dashboard

A demo-ready security operations dashboard for AWS, Azure, and GCP. The app is safe for public GitHub because it uses only synthetic alerts, incidents, assets, detections, playbooks, metrics, and executive reporting data.

## What this project is

This repository demonstrates how a multi-cloud SOC can collect cloud security findings, correlate incidents, track cloud asset risk, and explain operational risk to technical and non-technical stakeholders. It is designed for recruiter and interview demos on Windows with or without Docker.

## Architecture summary

- **Backend:** FastAPI app in `backend/app` with stable JSON endpoints under `/api`.
- **Frontend:** React, Vite, and TypeScript app in `frontend`.
- **Data:** In-memory synthetic multi-cloud SOC data only. No Postgres, Redis, cloud credentials, paid APIs, Docker, or external services are required for the local demo.
- **Docker:** Optional convenience path for reviewers who already have Docker installed.

## Windows no-Docker quickstart

Open two Command Prompt or PowerShell windows from the repo root.

### 1. Start the backend

```bat
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Start the frontend

```bat
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5174
```

### 3. Open the dashboard

Open: <http://127.0.0.1:5174>

You can also double-click `start-demo-windows.bat` from the repo root. It opens backend and frontend commands in separate windows.

## Docker quickstart

Docker is optional. If Docker Desktop is installed and running:

```bash
docker compose up --build backend frontend
```

Docker URLs:

- Dashboard: <http://127.0.0.1:5173>
- Backend docs: <http://127.0.0.1:8000/docs>
- Health: <http://127.0.0.1:8000/api/health>

## Demo URLs

- Local no-Docker dashboard: <http://127.0.0.1:5174>
- Backend docs: <http://127.0.0.1:8000/docs>
- Health endpoint: <http://127.0.0.1:8000/api/health>
- Alerts API: <http://127.0.0.1:8000/api/alerts>
- Incidents API: <http://127.0.0.1:8000/api/incidents>
- Metrics API: <http://127.0.0.1:8000/api/metrics>

## API endpoints

The backend exposes stable synthetic demo endpoints:

- `GET /api/health`
- `GET /api/alerts`
- `POST /api/alerts/ingest`
- `GET /api/incidents`
- `GET /api/assets`
- `GET /api/detections`
- `GET /api/playbooks`
- `GET /api/metrics`
- `GET /api/reports/executive-summary`

## Troubleshooting

### Docker is not recognized

Docker is not required. Use the Windows no-Docker quickstart above. If you want Docker support, install Docker Desktop and make sure it is running before using `docker compose`.

### npm is not recognized

Install Node.js LTS from <https://nodejs.org/>. Close and reopen your terminal after installation, then run `node --version` and `npm --version`.

### Blank white screen

The frontend is designed to show a warning instead of a blank screen if the backend is down. Check the terminal running `npm run dev` for compile errors, then confirm the backend health endpoint works at <http://127.0.0.1:8000/api/health>.

### Port already in use

Stop the program already using the port, or choose a different frontend port:

```bat
npm run dev -- --host 127.0.0.1 --port 5174
```

For the backend, free port `8000` or run uvicorn with another port and set `VITE_API_BASE_URL` for the frontend.

### Backend docs work but dashboard does not

`http://127.0.0.1:8000/docs` is the API documentation, not the React dashboard. Start the frontend and open `http://127.0.0.1:5174` for the local no-Docker dashboard.

## Interview demo script

1. **Open the dashboard:** “This is a synthetic multi-cloud SOC dashboard that consolidates AWS GuardDuty-style, Azure Defender/Sentinel-style, and GCP Security Command Center-style findings.”
2. **Show the KPI cards:** Explain open alerts, critical alerts, active incidents, asset inventory, and mean time to triage.
3. **Show severity and provider breakdowns:** “This helps analysts and managers understand where the current risk is concentrated across cloud providers.”
4. **Open recent alerts:** Point out severity, owner, status, and MITRE tactic/technique fields.
5. **Open incidents:** “Alerts are grouped into incidents so the SOC can investigate business impact instead of isolated events.”
6. **Show asset risk:** Tie cloud assets to risk levels and ownership for remediation accountability.
7. **Show detections and playbooks:** “Detection logic maps to SOC engineering, and playbooks map to repeatable incident response.”
8. **Show executive summary:** “This translates technical findings into business risk, recommended actions, and GRC/audit evidence.”
9. **Open API docs:** Visit `http://127.0.0.1:8000/docs` to show stable endpoints and safe synthetic data.

## Safety notes

- No real customer data is included.
- No real cloud credentials are required.
- No paid APIs are used.
- All dashboard content is synthetic and intended for demo, portfolio, and interview use.
