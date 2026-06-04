import json
import redis
import os
import logging

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None

def get_cache(key: str):
    if not redis_client:
        return None
    try:
        val = redis_client.get(key)
        if val:
            return json.loads(val)
    except Exception as e:
        logger.error(f"Redis get error for {key}: {e}")
    return None

import decimal

def default_serializer(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    return str(obj)

def set_cache(key: str, value: dict, ttl: int = 5):
    if not redis_client:
        return
    try:
        redis_client.setex(key, ttl, json.dumps(value, default=default_serializer))
    except Exception as e:
        logger.error(f"Redis set error for {key}: {e}")
