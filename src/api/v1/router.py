from fastapi import APIRouter
from src.api.v1.endpoints import auth

api_v1_router = APIRouter()

api_v1_router.include_router(
    auth.router,
    prefix="/authorization",
    tags=["authorization"]
)
