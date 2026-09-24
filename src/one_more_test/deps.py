"""Authentication and shared dependencies."""

from __future__ import annotations

from typing import Optional

from fastapi import Security
from auth_service_backend.fastapi_backend import FastAPIUser, FastAPIAuthServiceClient

from db.cache import redis_client


class RedisCacheAdapter:
    """Adapter to make redis.Redis compatible with CacheProtocol from auth_service_backend.

    The CacheProtocol expects set(key, value, timeout) but Redis uses set(key, value, ex=timeout).
    Also handles bytes encoding/decoding since redis_client has decode_responses=False.
    """

    def __init__(self, redis_client):
        self.redis = redis_client

    def get(self, key: str) -> Optional[str]:
        """Get a value from Redis cache, decoding bytes to string if needed."""
        value = self.redis.get(key)
        if value is None:
            return None
        return value.decode("utf-8") if isinstance(value, bytes) else value

    def set(self, key: str, value: str, timeout: int) -> None:
        """Set a value in Redis cache with expiration, encoding string to bytes if needed."""
        value_bytes = value.encode("utf-8") if isinstance(value, str) else value
        self.redis.set(key, value_bytes, ex=int(timeout))


auth_cache = RedisCacheAdapter(redis_client)
auth_client = FastAPIAuthServiceClient(cache=auth_cache)


def current_user_dep(scopes: list[str] | None = None):
    """
    Dependency factory that returns the current authenticated user.

    Use with FastAPI's Depends():
        user: FastAPIUser = Depends(current_user_dep(["example.read"]))
    """

    def dependency(
        current_user: FastAPIUser = Security(
            auth_client.get_current_user, scopes=scopes or []
        ),
    ) -> FastAPIUser:
        return current_user

    return dependency
