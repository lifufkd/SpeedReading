from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from src.core.exceptions import AppException


async def jwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
