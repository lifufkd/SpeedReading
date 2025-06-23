from fastapi import Depends

from src.services.auth import AuthService
from src.services.users import UsersService
from src.uow.abstract import AbstractUoW
from src.dependencies.uow import get_uow


async def get_auth_service(uow: AbstractUoW = Depends(get_uow)):
    return AuthService(uow)


async def get_users_service(uow: AbstractUoW = Depends(get_uow)):
    return UsersService(uow)
