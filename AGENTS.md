# AGENTS.md

## Cursor Cloud specific instructions

### Backend (FastAPI)

- **Working directory:** `/workspace/backend`
- **Run dev server:** `cd /workspace/backend && PYTHONPATH=/workspace/backend python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- **Run tests:** `cd /workspace/backend && PYTHONPATH=/workspace/backend python3 -m pytest -q`
- **Import check:** `cd /workspace/backend && PYTHONPATH=/workspace/backend python3 -c "from app.main import app; print('OK')"`
- **Database:** SQLite at `backend/soc.db` by default; set `DATABASE_URL` env var for Postgres.
- **Seeding:** The app auto-creates tables and seeds sample data (users, alerts, incidents, assets, detection rules, playbooks, audit entries) on startup if tables are empty.
- **Auth credentials (seed):** `admin/admin123` (admin), `analyst/analyst123` (analyst), `viewer/viewer123` (viewer).
- **bcrypt:** The environment uses `bcrypt<4.2` (pinned to 4.1.x) due to a breaking change in bcrypt 5.x with passlib. If you see `ValueError: password cannot be longer than 72 bytes`, ensure bcrypt is `<4.2`.
- **PYTHONPATH:** Always set `PYTHONPATH=/workspace/backend` when running backend commands, since the app uses absolute imports like `from app.main import app`.
- **API prefix:** All API routes are under `/api/` (e.g., `/api/health`, `/api/alerts`, `/api/auth/login`).
- **OpenAPI docs:** Available at `http://localhost:8000/docs` when the dev server is running.
