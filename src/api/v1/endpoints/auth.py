from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi import status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated

from src.core import jwt # noqa
from src.services.auth import AuthService
from src.dependencies.services import get_auth_service

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
async def login(
        request: Annotated[OAuth2PasswordRequestForm, Depends()],
        authorize: AuthJWT = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(
        username=request.username,
        password=request.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = authorize.create_access_token(subject=user.login)
    refresh_token = authorize.create_refresh_token(subject=user.login)

    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)
    return {"msg": "Login successful"}


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=dict)
async def refresh(
        authorize: AuthJWT = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )

    authorize.jwt_refresh_token_required()

    decoded_jwt = authorize.get_raw_jwt()
    await auth_service.revoke_jwt_token(decoded_jwt)

    user_name = authorize.get_jwt_subject()
    user = await auth_service.validate_user(user_name=user_name)
    if not user:
        raise credentials_exception

    new_access = authorize.create_access_token(subject=user.login)
    new_refresh = authorize.create_refresh_token(subject=user.login)

    authorize.set_access_cookies(new_access)
    authorize.set_refresh_cookies(new_refresh)
    return {"msg": "Token successfully refreshed"}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
        authorize: AuthJWT = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
):
    authorize.jwt_required()
    decoded_jwt = authorize.get_raw_jwt()

    await auth_service.revoke_jwt_token(decoded_jwt)
    authorize.unset_jwt_cookies()
