from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.uow.abstract import AbstractUoW
from src.core.config import jwt_settings
from src.models.users import Users
from src.schemas.users import UserSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(seconds=jwt_settings.ACCESS_TOKEN_EXPIRE_TIME)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, jwt_settings.JWT_SECRET_KEY, algorithm=jwt_settings.JWT_ALGORITHM)

    @staticmethod
    async def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_TIME)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, jwt_settings.JWT_SECRET_KEY, algorithm=jwt_settings.JWT_ALGORITHM)

    @staticmethod
    async def extract_user_name(token: str) -> str | None:
        try:
            payload = jwt.decode(token, jwt_settings.JWT_SECRET_KEY, algorithms=[jwt_settings.JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
        except JWTError:
            return None
        else:
            return username

    async def authenticate_user(self, username: str, password: str) -> UserSchema | None:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_name(name=username)
            if not user:
                return None
            if not await self.verify_password(password, user.password_hash):
                return None

            return UserSchema.model_validate(user)

    async def validate_user(self, token: str) -> UserSchema | None:
        user_name = await self.extract_user_name(token=token)
        if not user_name:
            return None
        async with self.uow as uow:
            user = await uow.user_repository.get_by_name(name=user_name)
            if not user:
                return None

            return UserSchema.model_validate(user)
