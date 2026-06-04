import re

with open('app/api/websocket.py', 'r') as f:
    code = f.read()

old_poll = """    async def poll_store(self, store_id: str):
        try:
            while True:
                # If no connections, exit task
                if not self.active_connections.get(store_id):
                    break
                    
                # We fetch all live required data
                live_data = await run_in_threadpool(get_live_dashboard, store_id)
                metrics_data = await run_in_threadpool(get_store_metrics, store_id)
                
                # Form the payload
                payload = {
                    "live": live_data,
                    "metrics": metrics_data,
                }
                
                message = json.dumps(payload, default=json_serializer)
                await self.broadcast(message, store_id)
                await asyncio.sleep(2)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Polling error for store {store_id}: {e}")"""

new_poll = """    async def poll_store(self, store_id: str):
        try:
            import os
            import redis.asyncio as aioredis
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            r = aioredis.from_url(redis_url, decode_responses=True)
            pubsub = r.pubsub()
            await pubsub.subscribe(f"store_update:{store_id}")
            
            # Initial fetch on connect
            live_data = await run_in_threadpool(get_live_dashboard, store_id)
            metrics_data = await run_in_threadpool(get_store_metrics, store_id)
            payload = {"live": live_data, "metrics": metrics_data}
            message = json.dumps(payload, default=json_serializer)
            await self.broadcast(message, store_id)
            
            async for message_in in pubsub.listen():
                if not self.active_connections.get(store_id):
                    break
                if message_in["type"] == "message":
                    live_data = await run_in_threadpool(get_live_dashboard, store_id)
                    metrics_data = await run_in_threadpool(get_store_metrics, store_id)
                    payload = {"live": live_data, "metrics": metrics_data}
                    message = json.dumps(payload, default=json_serializer)
                    await self.broadcast(message, store_id)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Pubsub error for store {store_id}: {e}")
        finally:
            if 'pubsub' in locals():
                await pubsub.close()
            if 'r' in locals():
                await r.close()"""

code = code.replace(old_poll, new_poll)

with open('app/api/websocket.py', 'w') as f:
    f.write(code)
