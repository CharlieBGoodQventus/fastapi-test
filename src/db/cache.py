"""Redis/Valkey client for auth token caching."""

import redis

from settings import settings

redis_client = redis.Redis(
    host=settings.valkey_host,
    port=settings.valkey_port,
    decode_responses=False,
    ssl=settings.valkey_ssl,
)
