import importlib
import os
import sys
from contextlib import contextmanager
from typing import Dict, Optional
from unittest.mock import patch

from fastapi.testclient import TestClient


@contextmanager
def app_with_env(env_vars: Optional[Dict[str, str]] = {}):
    """Context manager that imports the app with specified environment variables."""
    modules_to_clear = [
        "settings",
        "settings.base",
        "settings.local",
        "settings.prod",
    ]

    with patch.dict(os.environ, env_vars):
        for module in modules_to_clear:
            if module in sys.modules:
                del sys.modules[module]

        import fast_api_test.main

        importlib.reload(fast_api_test.main)

        yield fast_api_test.main.app


def test_status():
    """Test status endpoint with local environment (default)."""
    with app_with_env():
        from fast_api_test.main import app

        client = TestClient(app)
        resp = client.get("/status")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
        assert resp.json()["environment"] == "local"


def test_status_qa():
    """Test status endpoint with QA environment."""
    with app_with_env({"APP_ENV": "qa"}) as app:
        client = TestClient(app)
        resp = client.get("/status")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
        assert resp.json()["environment"] == "qa"


def test_status_prod():
    """Test status endpoint with production environment."""
    with app_with_env({"APP_ENV": "prod"}) as app:
        client = TestClient(app)
        resp = client.get("/status")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
        assert resp.json()["environment"] == "prod"
