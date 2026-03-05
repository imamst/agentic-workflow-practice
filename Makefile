start:
	uv run -m app.main

dev:
	uv run uvicorn app.fastapi-main:app --reload

celery:
	uv run celery -A app.celery_app worker --loglevel=info --pool=solo