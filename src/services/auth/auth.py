from datetime import datetime, timedelta

from src.services.users.users import UsersService
from src.uow.abstract import AbstractUoW
from src.core.redis_client import async_redis_client
from src.dto.users.auth import GetUserDTO
from src.core.jwt import verify_password
from src.core.orm_to_dto import sqlalchemy_to_pydantic


class AuthService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow
        self.users_service = UsersService(uow)

    @staticmethod
    async def revoke_jwt_token(decode_token: dict) -> None:
        jti = decode_token["jti"]
        exp = decode_token["exp"]
        ttl = exp - int(datetime.utcnow().timestamp())

        await async_redis_client.setex(jti, timedelta(seconds=ttl), "revoked")

    async def get_user_by_id(self, user_id: int) -> GetUserDTO | None:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                return None

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserDTO
            )
            return user

    async def authenticate_user(self, user_name: str, password: str) -> GetUserDTO | None:
        user = await self.users_service.get_by_name(name=user_name)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None

        return user
