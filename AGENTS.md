# AGENTS.md

## Cursor Cloud specific instructions

### Architecture

- **Backend**: Python 3.12 + FastAPI (stub endpoints, no DB wired yet). Source in `backend/app/`.
- **Frontend**: React 18 + TypeScript + Vite 6. Source in `frontend/src/`.
- Docker Compose is available (`docker-compose.yml`) but for local dev, run services natively as described below.

### Running services

**Backend** (port 8000):
```bash
cd backend
PYTHONPATH=/workspace/backend uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend** (port 5173):
```bash
cd frontend
npx vite --host 0.0.0.0 --port 5173
```

### Testing

**Backend tests** (requires `httpx` alongside packages in `requirements.txt`):
```bash
cd backend
PYTHONPATH=/workspace/backend pytest -q
```

**Frontend lint**:
```bash
cd frontend
npm run lint
```

### Gotchas

- `PYTHONPATH=/workspace/backend` must be set when running pytest or uvicorn outside Docker, since there is no `__init__.py` in `backend/app/` and no `setup.py`/`pyproject.toml`.
- `httpx` is required by `fastapi.testclient` / `starlette.testclient` but is not listed in `requirements.txt`. Install it alongside the other deps: `pip install httpx`.
- The frontend requires `vite.config.ts` with `@vitejs/plugin-react` configured for JSX to work without explicit `import React` statements. This file was added during setup.
- All backend API endpoints currently return hardcoded stubs (no database queries). PostgreSQL and Redis are defined in `docker-compose.yml` but not wired into app code.
- Swagger API docs are auto-generated at `http://localhost:8000/docs`.
