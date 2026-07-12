# News crawler microservice

This project implements a Dockerized news crawler assistant using FastAPI, Playwright, and a clean architecture layout under the src structure.

## Structure

- app/domain: entities and repository abstractions
- app/application: use cases such as NewsCrawlerService
- app/infrastructure: Playwright adapter implementation
- app/api: FastAPI routes and schema models
- app/config: runtime settings

## Run locally

```bash
uv sync --all-groups
uv run uvicorn app.main:app --host 0.0.0.0 --port 8002
```

## Run with Docker

```bash
docker compose up --build
```

The service exposes:

- POST /news/crawl

Example payload:

```json
{
  "url": "https://example.com"
}
```
