# fast-api-test

This is a test for a FastAPI

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

## Getting Started

```bash
# Install dependencies
uv sync --group dev

# Run the dev server
uv run uvicorn fast_api_test.main:app --reload --port 8080

# Or use docker-compose
docker-compose up
```

The API will be available at `http://localhost:8080`. Visit `/docs` for the interactive OpenAPI documentation.

## Development

```bash
# Run tests
uv run pytest

# Lint and format
uvx ruff check . && uvx ruff format .

# Full CI suite (tests + lint + security)
tox

# Security checks
uvx bandit -r src/
uvx safety check
```

## Project Structure

```
src/
├── fast_api_test/   # FastAPI app (main.py entry point)
├── settings/                     # Environment-aware config (base/local/prod)
└── <resource>/                   # Domain modules (router, model, schema, repository)
tests/
├── conftest.py                   # Shared test fixtures
└── test_main.py                  # App-level tests
```

## Configuration

Environment is selected via `APP_ENV` (defaults to `local`):

| Value   | Source            | Description                              |
|---------|-------------------|------------------------------------------|
| `local` | `.env` file       | Local development                        |
| `qa`    | Env vars / ESO    | QA/Staging (secrets from External Secrets)|
| `prod`  | Env vars / ESO    | Production (secrets from External Secrets)|

## Docker

```bash
# Build the image
docker build -t fast-api-test .

# Or use docker-compose for local development
docker-compose up
```

A Helm chart is included in `charts/fast-api-test/` for Kubernetes deployments.
