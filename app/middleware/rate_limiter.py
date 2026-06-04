from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.cache import redis_client

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def dispatch(self, request: Request, call_next):
        if not redis_client:
            return await call_next(request)
            
        # Optional: Skip rate limiting for health check
        if request.url.path == "/health":
            return await call_next(request)
            
        client_ip = request.client.host if request.client else "127.0.0.1"
        key = f"rate_limit:{client_ip}"
        
        try:
            current = redis_client.get(key)
            if current and int(current) >= self.max_requests:
                return JSONResponse(
                    status_code=429, 
                    content={"detail": "Too Many Requests - Rate Limit Exceeded"}
                )
                
            pipeline = redis_client.pipeline()
            pipeline.incr(key)
            pipeline.expire(key, self.window_seconds)
            pipeline.execute()
            
        except Exception:
            # Degrade gracefully if Redis fails
            pass
            
        response = await call_next(request)
        return response
