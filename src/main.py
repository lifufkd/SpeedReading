import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi_jwt_auth.exceptions import AuthJWTException

from src.database.init_db import create_tables
from src.api.v1.router import api_v1_router
from src.core.bootstrap import create_super_admin
from src.core.exceptions import AppException
from src.core.exceptions_handler import jwt_exception_handler, app_exception_handler


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    await create_super_admin()
    yield


app = FastAPI(lifespan=lifespan)

middleware = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_v1_router, prefix="/api/v1")

app.add_exception_handler(AuthJWTException, jwt_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
