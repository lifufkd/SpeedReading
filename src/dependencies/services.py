from fastapi import Depends

from src.services.auth import AuthService
from src.uow.abstract import AbstractUoW
from src.dependencies.uow import get_uow


async def get_auth_service(uow: AbstractUoW = Depends(get_uow)):
    return AuthService(uow)
