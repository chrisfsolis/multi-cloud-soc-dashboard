# Architecture

## Overview

The Multi-Cloud SOC Dashboard is a full-stack security operations platform built with a modern, layered architecture. It ingests alerts from AWS, Azure, and GCP, correlates them into incidents, runs automated response playbooks, and surfaces SOC metrics and compliance-ready reports.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Browser (React SPA)                      │
│  React 18 · TypeScript · Vite · Tailwind CSS · React Query      │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP / REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Nginx Reverse Proxy                         │
│                  (production) / Vite dev (local)                │
│                  routes /api/* → backend:8000                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend (Python)                     │
│                                                                 │
│  ┌───────────┐   ┌──────────┐   ┌──────────┐   ┌────────────┐ │
│  │ API Routes│──▶│ Schemas  │──▶│  Models  │──▶│  Database  │ │
│  │ (routers) │   │(Pydantic)│   │(SQLAlchemy)  │(PostgreSQL)│ │
│  └───────────┘   └──────────┘   └──────────┘   └────────────┘ │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐ │
│  │  Detection   │  │    SOAR      │  │   Metrics / Reports   │ │
│  │   Engine     │  │  Playbooks   │  │     Aggregation       │ │
│  └──────────────┘  └──────────────┘  └───────────────────────┘ │
└──────────┬──────────────────┬───────────────────────────────────┘
           │                  │
           ▼                  ▼
┌────────────────┐   ┌────────────────┐
│  PostgreSQL 16 │   │    Redis 7     │
│  (persistence) │   │   (caching,    │
│                │   │    sessions)   │
└────────────────┘   └────────────────┘
```

## Backend Layers

### API Routes (`app/api/`)

FastAPI routers organized by domain. Each module defines endpoints for a specific resource area:

| Module | Prefix | Responsibility |
|--------|--------|---------------|
| `health.py` | `/api/health` | Liveness and dependency checks |
| `alerts.py` | `/api/alerts` | Alert CRUD, ingestion, enrichment, search |
| `incidents.py` | `/api/incidents` | Incident management, notes, timeline, export |
| `assets.py` | `/api/assets` | Asset inventory, risk scoring |
| `detections.py` | `/api/detections` | Detection rule management, testing, reload |
| `playbooks.py` | `/api/playbooks` | SOAR playbook execution, approval, runs |
| `metrics.py` | `/api/metrics` | SOC KPIs (MTTD, MTTA, MTTR, volumes) |
| `reports.py` | `/api/reports` | Incident reports, executive summary, monthly |
| `audit.py` | `/api/audit` | Audit trail queries |

### Schemas (Pydantic)

Request/response validation models enforcing type safety, field constraints, and serialization. Schemas decouple the API contract from the database models.

### Models (SQLAlchemy)

ORM models mapping to PostgreSQL tables. See [Data Model](data-model.md) for the full schema reference.

### Database (PostgreSQL 16)

Primary relational store for all persistent data: users, alerts, incidents, assets, detection rules, playbooks, playbook runs, and audit entries.

### Cache (Redis 7)

Used for session storage, rate limiting counters, and caching expensive metric aggregations.

## Frontend Architecture

```
src/
├── components/        # Reusable UI components
├── pages/             # Route-level page components
├── hooks/             # Custom React hooks (useAlerts, useAuth, etc.)
├── api/               # API client (fetch wrappers, React Query)
├── types/             # TypeScript type definitions
├── utils/             # Helpers and formatters
├── App.tsx            # Root component with routing
└── main.tsx           # Entry point
```

**Key libraries:**

| Library | Purpose |
|---------|---------|
| React 18 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool and dev server |
| Tailwind CSS | Utility-first styling |
| React Query | Server-state management and caching |
| React Router v6 | Client-side routing |
| Recharts | Data visualization / charts |

## Authentication & Authorization

- **JWT-based authentication**: Users authenticate via `/api/auth/login` and receive a signed JWT. The token is sent in the `Authorization: Bearer <token>` header on subsequent requests.
- **Role-Based Access Control (RBAC)**: Three roles with escalating permissions:

| Role | Permissions |
|------|------------|
| `viewer` | Read-only access to dashboards, alerts, incidents |
| `analyst` | Viewer + create/update incidents, run playbooks, add notes |
| `admin` | Analyst + user management, detection rule reload, audit access |

## Data Flow

```
Cloud Providers (AWS/Azure/GCP)
        │
        ▼
  Alert Ingest API (/api/alerts/ingest)
        │
        ▼
  Normalization (provider-specific → common schema)
        │
        ▼
  Storage (PostgreSQL)
        │
        ├──▶ Detection Engine (YAML rules evaluated)
        │         │
        │         ▼
        │    Auto-create Incidents
        │
        ├──▶ IOC Enrichment (IP/domain/hash lookups)
        │
        ├──▶ SOAR Playbooks (automated response)
        │         │
        │         ▼
        │    Approval → Execution → Completion
        │
        └──▶ Metrics Aggregation → Dashboard
                                  → Reports
```

### Alert Lifecycle

1. **Ingest** — Raw cloud alert received via API or sample data load
2. **Normalize** — Map provider-specific fields to the common alert schema
3. **Detect** — Run detection rules; auto-escalate matches to incidents
4. **Enrich** — IOC enrichment adds threat intel context
5. **Triage** — Analyst reviews, assigns, updates status
6. **Resolve** — Alert closed as resolved or false positive

### Incident Lifecycle

1. **Create** — Manually from correlated alerts or auto-created by detection rules
2. **Investigate** — Analyst reviews timeline, adds notes, assigns
3. **Respond** — Trigger SOAR playbooks for automated response
4. **Resolve** — Close incident, generate report
5. **Audit** — Full audit trail recorded for compliance

## Deployment

See the root [docker-compose.yml](../docker-compose.yml) for the complete stack definition. The production setup uses:

- **Backend**: Python 3.12 slim image, non-root `soc` user, health checks
- **Frontend**: Multi-stage build (Node 20 build → Nginx serve), reverse proxy to backend
- **PostgreSQL 16**: Persistent volume, health checks
- **Redis 7**: Session cache, health checks
