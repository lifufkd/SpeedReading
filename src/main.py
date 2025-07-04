import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi_jwt_auth.exceptions import AuthJWTException

from src.database.init_db import create_tables
from src.api.v1.router import api_v1_router
from src.core.bootstrap import create_super_admin, disable_default_logging
from src.core.exceptions import AppException
from src.core.exceptions_handler import jwt_exception_handler, app_exception_handler, internal_server_error_handler
from src.core.config import cors_settings
from src.core.middleware import LoggingMiddleware
from src.core.logger import setup_logger


@asynccontextmanager
async def lifespan(_: FastAPI):
    await disable_default_logging()
    setup_logger()
    await create_tables()
    await create_super_admin()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=cors_settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=cors_settings.CORS_ALLOW_METHODS,
    allow_headers=cors_settings.CORS_ALLOW_HEADERS,
)
app.add_middleware(LoggingMiddleware)

app.include_router(api_v1_router, prefix="/api/v1")

app.add_exception_handler(AuthJWTException, jwt_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, internal_server_error_handler)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
