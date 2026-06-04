from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from app.api.live import get_live_dashboard
from app.services.metrics_service import get_store_metrics
from starlette.concurrency import run_in_threadpool
import json
from decimal import Decimal

router = APIRouter()

def json_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.polling_tasks: dict[str, asyncio.Task] = {}

    async def connect(self, websocket: WebSocket, store_id: str):
        await websocket.accept()
        if store_id not in self.active_connections:
            self.active_connections[store_id] = []
        self.active_connections[store_id].append(websocket)
        
        # Start polling task for this store if not running
        if store_id not in self.polling_tasks or self.polling_tasks[store_id].done():
            self.polling_tasks[store_id] = asyncio.create_task(self.poll_store(store_id))

    def disconnect(self, websocket: WebSocket, store_id: str):
        if store_id in self.active_connections:
            if websocket in self.active_connections[store_id]:
                self.active_connections[store_id].remove(websocket)
            if not self.active_connections[store_id]:
                del self.active_connections[store_id]
                # Stop polling task if no clients left
                if store_id in self.polling_tasks:
                    self.polling_tasks[store_id].cancel()
                    del self.polling_tasks[store_id]

    async def broadcast(self, message: str, store_id: str):
        connections = self.active_connections.get(store_id, [])
        dead_connections = []
        for connection in connections:
            try:
                await connection.send_text(message)
            except Exception:
                dead_connections.append(connection)
                
        for dead in dead_connections:
            self.disconnect(dead, store_id)

    async def poll_store(self, store_id: str):
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
                await r.close()

manager = ConnectionManager()

@router.websocket("/websocket/live/{store_id}")
async def websocket_endpoint(websocket: WebSocket, store_id: str):
    await manager.connect(websocket, store_id)
    try:
        while True:
            # Just keep the connection alive and handle client disconnects
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, store_id)

