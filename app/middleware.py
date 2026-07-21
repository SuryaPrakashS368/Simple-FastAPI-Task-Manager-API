import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = round(time.time() - start, 3)
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} - {duration}s"
        )
        return response