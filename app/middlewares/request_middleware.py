"""
Middleware personalizado de trazabilidad.
Agrega cabeceras X-App-Name, X-Process-Time, X-Request-ID a cada respuesta
y registra método, ruta y código de estado en el log.
"""
import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("device_systems")


class RequestMiddleware(BaseHTTPMiddleware):
    """
    Middleware global que:
    - Mide tiempo de respuesta.
    - Agrega cabecera X-Process-Time.
    - Agrega cabecera X-App-Name: device_systems.
    - Genera o propaga X-Request-ID.
    - Registra método, ruta y código de estado.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()

        request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex[:8])

        response: Response = await call_next(request)

        process_time = round(time.perf_counter() - start_time, 4)

        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id

        logger.info(
            f"{request.method} | {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time}s | Request-ID: {request_id}"
        )

        return response
