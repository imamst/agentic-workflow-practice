start:
	uv run -m app.main

dev:
	uv run uvicorn app.fastapi-main:app --reload