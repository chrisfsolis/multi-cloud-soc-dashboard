# Multi-Cloud SOC Dashboard

Advanced multi-cloud Security Operations Center (SOC) dashboard combining AWS, Azure, and GCP alert ingestion with SIEM-style detection, incident correlation, SOAR playbooks, SOC metrics, and audit-ready reporting.

## Features

- [x] **Multi-cloud alert ingestion** — Unified pipeline for AWS GuardDuty, Azure Sentinel, GCP SCC
- [x] **Alert normalization** — Common schema with MITRE ATT&CK mapping
- [x] **IOC enrichment** — IP reputation, domain lookup, hash analysis
- [x] **Incident correlation** — Cross-provider incident management with timeline
- [x] **YAML detection rules** — Custom detection engine with auto-escalation
- [x] **SOAR playbooks** — Automated response with approval workflows
- [x] **SOC metrics** — MTTD, MTTA, MTTR, false positive rate, alert/incident volume
- [x] **Compliance reports** — Executive summaries, incident reports, monthly SOC reports
- [x] **Role-based access** — Admin, analyst, viewer roles with JWT authentication
- [x] **Full audit trail** — Immutable audit log for all state changes
- [x] **Asset inventory** — Cloud resource tracking with risk scoring
- [x] **REST API** — Complete API with interactive Swagger documentation

## Architecture

```
Browser (React) → Nginx → FastAPI → PostgreSQL
                                   → Redis
```

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, React Query, React Router
- **Backend**: FastAPI (Python 3.12), SQLAlchemy, Pydantic
- **Database**: PostgreSQL 16
- **Cache**: Redis 7

See [docs/architecture.md](docs/architecture.md) for the full architecture documentation.

## Quick Start

### Docker (recommended)

```bash
# Start all services
make up

# Seed the database with synthetic data
make seed

# Open the dashboard
open http://localhost:5173

# View API docs
open http://localhost:8000/docs
```

### Local Development

**Backend:**

```bash
cd backend
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**

```bash
cd frontend
npm install
npx vite --host 0.0.0.0 --port 5173
```

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin123` | Admin |

## API Documentation

Interactive Swagger docs are available at [http://localhost:8000/docs](http://localhost:8000/docs) when the backend is running.

See [docs/api-reference.md](docs/api-reference.md) for the full API reference.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript 5, Vite 6, Tailwind CSS |
| Backend | Python 3.12, FastAPI, SQLAlchemy, Pydantic |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Auth | JWT (JSON Web Tokens), bcrypt |
| Detection | Custom YAML rule engine |
| SOAR | Built-in playbook execution engine |
| Containerization | Docker, Docker Compose |

## Project Structure

```
multi-cloud-soc-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI route modules
│   │   │   ├── alerts.py
│   │   │   ├── assets.py
│   │   │   ├── audit.py
│   │   │   ├── detections.py
│   │   │   ├── health.py
│   │   │   ├── incidents.py
│   │   │   ├── metrics.py
│   │   │   ├── playbooks.py
│   │   │   └── reports.py
│   │   └── main.py           # FastAPI application entry point
│   ├── detection_rules/      # YAML detection rule definitions
│   ├── synthetic_data/       # Sample data for demos
│   ├── tests/                # Backend test suite
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx           # Root component
│   │   └── main.tsx          # Entry point
│   ├── Dockerfile
│   ├── nginx.conf            # Production reverse proxy config
│   ├── index.html
│   └── package.json
├── docs/
│   ├── api-reference.md      # API endpoint documentation
│   ├── architecture.md       # System architecture
│   ├── data-model.md         # Database schema reference
│   ├── detection-rules.md    # Detection rule format and examples
│   ├── soar-playbooks.md     # SOAR playbook documentation
│   ├── recruiter-demo-guide.md  # Live demo walkthrough
│   └── screenshots.md        # Planned UI screenshots
├── docker-compose.yml        # Full stack orchestration
├── Makefile                  # Development commands
├── SECURITY.md
├── CONTRIBUTING.md
└── README.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, workflow, and guidelines.

## License

MIT
