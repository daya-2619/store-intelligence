import os
import json
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
except Exception:
    redis_client = None

class RedisDict:
    def __init__(self, name):
        self.name = name

    def __getitem__(self, key):
        if not redis_client: return None
        val = redis_client.hget(self.name, str(key))
        if val is None:
            raise KeyError(key)
        return json.loads(val)

    def __setitem__(self, key, value):
        if redis_client:
            redis_client.hset(self.name, str(key), json.dumps(value))

    def __delitem__(self, key):
        if redis_client:
            redis_client.hdel(self.name, str(key))

    def __contains__(self, key):
        if not redis_client: return False
        return redis_client.hexists(self.name, str(key))

    def get(self, key, default=None):
        if not redis_client: return default
        val = redis_client.hget(self.name, str(key))
        return json.loads(val) if val is not None else default

    def keys(self):
        if not redis_client: return []
        return redis_client.hkeys(self.name)

    def items(self):
        if not redis_client: return []
        return {k: json.loads(v) for k, v in redis_client.hgetall(self.name).items()}.items()

class RedisSet:
    def __init__(self, name):
        self.name = name

    def add(self, value):
        if redis_client:
            redis_client.sadd(self.name, str(value))

    def remove(self, value):
        if redis_client:
            redis_client.srem(self.name, str(value))

    def __contains__(self, value):
        if not redis_client: return False
        return redis_client.sismember(self.name, str(value))

class RedisCounter:
    def __init__(self, name):
        self.name = name

    @property
    def value(self):
        if not redis_client: return 0
        val = redis_client.get(self.name)
        return int(val) if val else 0

    def increment(self):
        if not redis_client: return 0
        return redis_client.incr(self.name)

    def __add__(self, other):
        return self.increment()
        
    def __iadd__(self, other):
        return self.increment()

# Re-ID Globals
global_id_counter_obj = RedisCounter("global_id_counter")

class StoreStateManager:
    def __init__(self, store_id: str):
        self.store_id = store_id
        
        self.visitor_zone_state = RedisDict(f"{store_id}:visitor_zone_state")
        self.active_tracks = RedisDict(f"{store_id}:active_tracks")
        self.missing_frames = RedisDict(f"{store_id}:missing_frames")
        self.zone_entry_time = RedisDict(f"{store_id}:zone_entry_time")
        self.track_positions = RedisDict(f"{store_id}:track_positions")
        self.queue_state = RedisDict(f"{store_id}:queue_state")
        self.staff_candidates = RedisDict(f"{store_id}:staff_candidates")
        self.visitor_last_seen = RedisDict(f"{store_id}:visitor_last_seen")
        self.reentry_window = RedisDict(f"{store_id}:reentry_window")
        self.dwell_sent = RedisDict(f"{store_id}:dwell_sent")
        self.visitor_confidence = RedisDict(f"{store_id}:visitor_confidence")
        self.last_dwell_emit_time = RedisDict(f"{store_id}:last_dwell_emit_time")
        
        # Re-ID Globals per store
        self.global_embeddings = RedisDict(f"{store_id}:global_embeddings")
        self.local_to_global = RedisDict(f"{store_id}:local_to_global")
        self.exited_globals = RedisSet(f"{store_id}:exited_globals")
        
        # Stage 3
        self.queue_start_time = RedisDict(f"{store_id}:queue_start_time")
        self.visitor_purchased = RedisDict(f"{store_id}:visitor_purchased")
        
        self.heatmap_points = []