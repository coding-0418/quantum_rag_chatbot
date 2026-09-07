.PHONY: install run test lint up down ingest

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest --cov=app --cov-report=term-missing tests/

lint:
	ruff check app tests

up:
	docker compose up --build

down:
	docker compose down -v

ingest:
	python scripts/ingest_knowledge_base.py
