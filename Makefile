up:
	docker compose up --build -d
down:
	docker compose down
seed:
	docker compose exec backend python -m app.utils.seed_data
test:
	docker compose exec backend pytest -q
test-local:
	cd backend && PYTHONPATH=. pytest -v
lint:
	cd backend && ruff check app/ tests/ || true
	cd frontend && npm run lint
dev-backend:
	cd backend && PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
dev-frontend:
	cd frontend && npx vite --host 0.0.0.0 --port 5173
