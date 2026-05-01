up:
	docker compose up --build -d
down:
	docker compose down
seed:
	docker compose exec backend python -m app.utils.seed_data
test:
	docker compose exec backend pytest -q
