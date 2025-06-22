from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext

from src.core.redis_client import sync_redis_client
from src.core.config import jwt_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@AuthJWT.load_config
def get_config():
    return jwt_settings


@AuthJWT.token_in_denylist_loader
def token_in_denylist(decoded_token):
    jti = decoded_token.get("jti")
    return sync_redis_client.exists(jti)
