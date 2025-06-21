from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

from src.services.auth import AuthService
from src.dependencies.services import get_auth_service
from src.models.users import Users


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def validate_token(
        token: str = Depends(oauth2_scheme),
        service: AuthService = Depends(get_auth_service)
) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await service.validate_user(token=token)
    if not user:
        raise credentials_exception

    return user
