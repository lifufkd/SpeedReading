from datetime import datetime, timedelta

from src.uow.abstract import AbstractUoW
from src.core.redis_client import async_redis_client
from src.schemas.users import UserSchema
from src.core.jwt import pwd_context


class AuthService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def revoke_jwt_token(decode_token: dict) -> None:
        jti = decode_token["jti"]
        exp = decode_token["exp"]
        ttl = exp - int(datetime.utcnow().timestamp())

        await async_redis_client.setex(jti, timedelta(seconds=ttl), "revoked")

    async def authenticate_user(self, username: str, password: str) -> UserSchema | None:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_name(name=username)
            if not user:
                return None
            if not await self.verify_password(password, user.password_hash):
                return None

            return UserSchema.model_validate(user)

    async def validate_user(self, user_name: str) -> UserSchema | None:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_name(name=user_name)
            if not user:
                return None

            return UserSchema.model_validate(user)
