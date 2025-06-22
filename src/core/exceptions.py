from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException


def register_exception_handler(app: FastAPI):

    @app.exception_handler(AuthJWTException)
    def jwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})