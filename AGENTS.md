# AGENTS.md

FastAPI service (Python 3.10) with pydantic-settings and Helm chart for Kubernetes deployment.

## Commands

```bash
uv sync --group dev                          # Setup
uv run uvicorn fast_api_test.main:app --reload --port 8080  # Dev server
uv run pytest -q                             # Tests
uvx ruff check . && uvx ruff format .        # Lint/format
tox                                          # Full CI
```

## Structure

```
src/
├── fast_api_test/   # FastAPI app (main.py), entry point
├── <resource>/                   # model.py, repository.py, router.py, schema.py
└── settings/                     # base.py, local.py, prod.py (APP_ENV selects)
```

## Patterns

**New Resource**: Create `src/<resource>/` with model, repository, router, schema. Router uses `Depends()` for dependency injection. Include in `main.py` with `/v1` prefix.

```python
# router.py
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/items")
def list_items():
    ...
```

Register in `main.py`:

```python
from my_resource import router as my_resource_router

app.include_router(
    my_resource_router.router,
    prefix="/v1",
    tags=["my-resource"],
)
```

## Settings

`APP_ENV` environment variable selects the settings module:

- **local**: Reads from `.env` file via pydantic-settings
- **qa/prod**: Reads from environment variables and ESO file-mounted secrets at `/etc/secrets`

Add shared fields in `src/settings/base.py`. Use `read_secret()` for values that come from External Secrets Operator.

## Testing

Tests in `tests/<resource>/`. Use `httpx` + `TestClient` from FastAPI. Shared fixtures in `conftest.py`.

```python
from fastapi.testclient import TestClient
from fast_api_test.main import app

client = TestClient(app)
resp = client.get("/v1/items")
```

## Dependencies

`uv` with `pyproject.toml`. Use `uv sync --frozen --group dev` for reproducible installs. CI via `tox-uv`: tests, ruff-check, ruff-format, bandit, safety.
