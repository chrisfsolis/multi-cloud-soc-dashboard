# Enhancement Backlog

Prioritized backlog for the Multi-Cloud SOC Dashboard, organized by dependency tier.

---

## Tier 1 — Foundation (unblocks everything else)

| # | Enhancement | Scope | Why first |
|---|------------|-------|-----------|
| 1 | **Pydantic request/response schemas** | All 44 endpoints | Raw `dict` bodies have zero validation; schemas unlock OpenAPI docs, client codegen, and input safety |
| 2 | **SQLAlchemy models + Alembic migrations** | `backend/app/models/`, `alembic/` | No persistence layer exists despite Postgres in docker-compose |
| 3 | **Wire Postgres connection** | `main.py` lifespan, settings module | `.env.example` defines `DATABASE_URL` but nothing reads it; add `pydantic-settings` config loader |
| 4 | **Seed data module** | `backend/app/utils/seed_data.py` | `make seed` references a module that doesn't exist |
| 5 | **Fix `/alerts/search` route ordering** | `alerts.py` | `{alert_id}` is registered before `/search`, so `GET /api/alerts/search` resolves to `alert_id="search"` |

## Tier 2 — Cross-cutting Backend Concerns

| # | Enhancement | Scope |
|---|------------|-------|
| 6 | **Auth + RBAC** | JWT/OAuth middleware, role-based route guards, login endpoint |
| 7 | **CORS middleware** | `main.py` — required once the frontend calls the API from a browser |
| 8 | **Pagination + filtering** | All list endpoints — add `limit`/`offset`/`cursor` query params |
| 9 | **Global error handling** | Exception handlers for 404, 422, 500; consistent error response schema |
| 10 | **Request logging + correlation IDs** | Middleware for structured logging with request tracing |
| 11 | **Rate limiting** | Especially on `/alerts/ingest` and auth endpoints |

## Tier 3 — Domain Logic

Each item has a corresponding template and/or synthetic data example under `backend/synthetic_data/`. Detection rule templates are under `backend/detection_rules/`.

| # | Enhancement | Template | Synthetic data |
|---|------------|----------|----------------|
| 12 | **Alert ingestion + normalization** | Multi-cloud payload normalization | `alerts_ingest.json` |
| 13 | **Detection rule engine** | YAML rule definitions | `detection_test_result.json` + `detection_rules/*.yml` |
| 14 | **Incident correlation** | Auto-group alerts by asset/time/technique | `incidents.json` |
| 15 | **Playbook execution engine** | Step runner with approval gates | `playbooks.json` |
| 16 | **Metrics aggregation** | Time-range KPI computation | `metrics.json` |
| 17 | **Report generation** | Markdown/PDF incident + executive reports | `reports.json` |
| 18 | **Alert enrichment** | Threat intel + asset context lookups | `enrichment.json` |
| 19 | **Health dependency probes** | Probe Postgres, Redis, external APIs | `health_dependencies.json` |
| 20 | **Audit trail** | Immutable append-only mutation log | `audit.json` |

## Tier 4 — Frontend

| # | Enhancement | Scope |
|---|------------|-------|
| 21 | **Route map + layout shell** | Sidebar nav, header, Routes for each domain |
| 22 | **API client layer** | Axios/fetch wrapper + React Query hooks |
| 23 | **Dashboard page** | KPI cards, alert volume chart, incident status breakdown |
| 24 | **Alerts table + detail view** | Sortable/filterable table, detail modal with enrichment |
| 25 | **Incidents management UI** | Create, triage, assign, add notes, view timeline |
| 26 | **SOAR playbook UI** | Playbook catalog, run wizard, approval flow |
| 27 | **Styling framework** | Tailwind / MUI / Shadcn — replace inline styles |
| 28 | **Auth UI** | Login page, session management, role-based nav |
| 29 | **Real ESLint + Prettier** | Replace `"lint": "echo lint"` with real linting |
| 30 | **`tsconfig.json`** | Add strict TypeScript configuration |

## Tier 5 — Testing + CI

| # | Enhancement | Scope |
|---|------------|-------|
| 31 | **Backend test coverage** | 43 of 44 endpoints untested; add parametrized happy + error tests |
| 32 | **Frontend tests** | Vitest + React Testing Library |
| 33 | **CI lint workflow** | `.github/workflows/lint.yml` is a stub — wire real linters |
| 34 | **CI Postgres service container** | Backend test workflow needs Postgres for integration tests |
| 35 | **Dependency scanning** | `pip-audit` / `npm audit` in CI |
| 36 | **Coverage gates** | Fail CI below threshold; report coverage on PRs |

## Tier 6 — DevOps + Docs

| # | Enhancement | Scope |
|---|------------|-------|
| 37 | **Docker Compose hardening** | Env vars, `depends_on`, healthchecks, volumes, non-root users |
| 38 | **Production frontend Dockerfile** | `npm run build` + nginx instead of Vite dev server |
| 39 | **Fill all `docs/*.md` stubs** | 7 files are title-only |
| 40 | **README overhaul** | Setup instructions, architecture diagram, screenshots |
| 41 | **SECURITY.md policy** | Vulnerability disclosure, supported versions, auth model |
| 42 | **CONTRIBUTING.md expansion** | Branch strategy, code style, commit conventions |
| 43 | **Redis integration** | Caching metrics, rate limiting, pub/sub alert streaming |
| 44 | **WebSocket/SSE live alerts** | Real-time alert feed to frontend dashboard |
