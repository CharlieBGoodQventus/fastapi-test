"""Settings module with automatic environment detection.

The environment is determined by the APP_ENV environment variable.
Valid values: local, qa, prod (defaults to local)
"""

import os

APP_ENV = os.environ.get("APP_ENV", "local").lower()

if APP_ENV == "qa" or APP_ENV == "prod":
    from settings.prod import settings
elif APP_ENV == "local":
    from settings.local import settings
else:
    raise ValueError(
        f"Invalid APP_ENV value: {APP_ENV}. Must be one of: local, qa, prod"
    )

__all__ = ["settings"]
