from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext

from src.core.redis_client import sync_redis_client
from src.core.config import jwt_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@AuthJWT.load_config
def get_config():
    return jwt_settings


@AuthJWT.token_in_denylist_loader
def token_in_denylist(decoded_token):
    jti = decoded_token.get("jti")
    return sync_redis_client.exists(jti)
