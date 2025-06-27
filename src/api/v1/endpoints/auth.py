from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi import status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated

from src.core import jwt # noqa
from src.services.auth.auth import AuthService
from src.dependencies.services import get_auth_service
from src.core.exceptions import UserNotFound
from src.core.dto_to_schema import dto_to_schema
from src.schemas.users.auth import UserSchema

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def login(
        request: Annotated[OAuth2PasswordRequestForm, Depends()],
        authorize: AuthJWT = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(
        user_name=request.username,
        password=request.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = authorize.create_access_token(subject=user.login, user_claims={"user_id": user.user_id})
    refresh_token = authorize.create_refresh_token(subject=user.login)

    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)

    user = await dto_to_schema(
        user,
        UserSchema
    )
    return user


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def refresh(
        authorize: AuthJWT = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
):
    authorize.jwt_refresh_token_required()

    decoded_jwt = authorize.get_raw_jwt()
    await auth_service.revoke_jwt_token(decoded_jwt)

    user_name = authorize.get_jwt_subject()
    user = await auth_service.users_service.get_by_name(name=user_name)
    if not user:
        raise UserNotFound()

    new_access = authorize.create_access_token(subject=user.login, user_claims={"user_id": user.user_id})
    new_refresh = authorize.create_refresh_token(subject=user.login)

    authorize.set_access_cookies(new_access)
    authorize.set_refresh_cookies(new_refresh)

    user = await dto_to_schema(
        user,
        UserSchema
    )
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
        authorize: AuthJWT = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
):
    authorize.jwt_required()
    decoded_jwt = authorize.get_raw_jwt()

    await auth_service.revoke_jwt_token(decoded_jwt)
    authorize.unset_jwt_cookies()
