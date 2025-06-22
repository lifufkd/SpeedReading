from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from fastapi_jwt_auth import AuthJWT

from src.services.auth import AuthService
from src.dependencies.services import get_auth_service
from src.schemas.users import UserSchema


async def validate_token(
        authorize: AuthJWT = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    authorize.jwt_required()

    user_name = authorize.get_jwt_subject()
    user = await auth_service.validate_user(user_name=user_name)
    if not user:
        raise credentials_exception

    return user
