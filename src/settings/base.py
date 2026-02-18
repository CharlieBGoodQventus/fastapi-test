"""Base settings class with common configuration for all environments."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Literal, Optional

from pydantic import Field
from pydantic_settings import BaseSettings

SECRETS_PATH = Path(os.getenv("SECRETS_PATH", "/etc/secrets"))


def read_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    """Read a secret from file (ESO) or fall back to environment variable.

    External Secrets Operator mounts secrets as files at SECRETS_PATH/<name>.
    This function tries to read from file first, then falls back to env var.

    Args:
        name: The secret name (file name in SECRETS_PATH, or env var name)
        default: Default value if secret is not found

    Returns:
        The secret value, or default if not found
    """
    secret_file = SECRETS_PATH / name
    if secret_file.exists():
        return secret_file.read_text().strip()
    return os.getenv(name, default)


def read_json_secret(name: str) -> Optional[Dict[str, Any]]:
    """Read a JSON secret from file (ESO) and parse it.

    For Secrets Manager secrets that contain JSON objects.

    Args:
        name: The secret name (file name in SECRETS_PATH)

    Returns:
        Parsed JSON as dict, or None if not found
    """
    value = read_secret(name)
    if value:
        return json.loads(value)
    return None


class Settings(BaseSettings):
    """Base settings class with fields common to all environments."""

    env: Literal["local", "qa", "prod"] = Field(default="local", alias="APP_ENV")

    # Add your shared settings fields here, for example:
    # DATABASE_URL: str = Field(default="sqlite:///./dev.db")
    # API_KEY: str = Field(default="dev-key")
