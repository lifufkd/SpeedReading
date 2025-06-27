from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from src.services.auth.auth import AuthService
from src.dependencies.services import get_auth_service
from src.core.exceptions import UserNotFound
from src.dto.users import GetUsersDTO
from src.schemas.enums import UsersRoles
from src.core.exceptions import UserIsNotAdmin, JWTError


async def validate_token(
        authorize: AuthJWT = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
) -> GetUsersDTO:
    authorize.jwt_required()

    claims = authorize.get_raw_jwt()
    if not isinstance(claims.get('user_id'), int):
        raise JWTError()

    user = await auth_service.get_user_by_id(user_id=int(claims["user_id"]))
    if not user:
        raise UserNotFound()

    return user


async def validate_admin(current_user: GetUsersDTO = Depends(validate_token)) -> None:
    if current_user.role != UsersRoles.ADMIN:
        raise UserIsNotAdmin()
