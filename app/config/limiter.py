"""
Rate limiting sin dependencias externas.
Implementa una ventana deslizante por IP, compatible con la interfaz de slowapi:
    @limiter.limit("5/minute")

Uso:
    from app.config.limiter import limiter
    # En main.py:
    app.state.limiter = limiter
"""
import time
from collections import defaultdict, deque
from threading import Lock
from functools import wraps

from fastapi import Request, HTTPException, status


class _RateLimiter:
    """Implementación de rate limiter con ventana deslizante en memoria."""

    def __init__(self):
        self._store: dict = defaultdict(deque)
        self._lock = Lock()

    def _parse_limit(self, limit_string: str) -> tuple[int, int]:
        """Parsea '5/minute', '30/minute', '10/minute' → (max_requests, window_seconds)"""
        parts = limit_string.strip().split("/")
        max_req = int(parts[0])
        unit = parts[1].lower() if len(parts) > 1 else "minute"
        windows = {"second": 1, "minute": 60, "hour": 3600}
        return max_req, windows.get(unit, 60)

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def _check(self, key: str, max_requests: int, window_seconds: int) -> None:
        now = time.time()
        with self._lock:
            dq = self._store[key]
            while dq and dq[0] < now - window_seconds:
                dq.popleft()
            if len(dq) >= max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Demasiadas solicitudes. Límite: {max_requests} por {window_seconds}s.",
                    headers={"Retry-After": str(window_seconds)},
                )
            dq.append(now)

    def limit(self, limit_string: str):
        """
        Decorador compatible con la firma de slowapi:
            @limiter.limit("5/minute")
            def endpoint(request: Request, ...):
        """
        max_req, window = self._parse_limit(limit_string)

        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                request = kwargs.get("request") or next(
                    (a for a in args if isinstance(a, Request)), None
                )
                if request:
                    ip = self._get_client_ip(request)
                    key = f"{func.__name__}:{ip}"
                    self._check(key, max_req, window)
                return await func(*args, **kwargs)

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                request = kwargs.get("request") or next(
                    (a for a in args if isinstance(a, Request)), None
                )
                if request:
                    ip = self._get_client_ip(request)
                    key = f"{func.__name__}:{ip}"
                    self._check(key, max_req, window)
                return func(*args, **kwargs)

            import asyncio
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper

        return decorator


limiter = _RateLimiter()
