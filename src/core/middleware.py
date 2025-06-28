from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        logger.info(f"Request: {request.method} {request.url}")

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(f"Response: {request.method} {request.url} completed in {process_time:.2f}s with status {response.status_code}")
        return response
