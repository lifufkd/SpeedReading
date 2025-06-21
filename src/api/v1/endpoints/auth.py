from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import status, Depends, Body
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

from src.services.auth import AuthService
from src.dependencies.services import get_auth_service
from src.schemas.token import Token

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(
        request: Annotated[OAuth2PasswordRequestForm, Depends()],
        service: AuthService = Depends(get_auth_service)
):
    user = await service.authenticate_user(
        username=request.username,
        password=request.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = await service.create_access_token(data={"sub": user.login})
    refresh_token = await service.create_refresh_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=Token)
async def refresh(
        refresh_token: str = Body(),
        service: AuthService = Depends(get_auth_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token invalid",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await service.validate_user(token=refresh_token)
    if not user:
        raise credentials_exception

    new_access_token = await service.create_access_token(data={"sub": user.login})
    new_refresh_token = await service.create_refresh_token(data={"sub": user.login})
    return {"access_token": new_access_token, "token_type": "bearer", "refresh_token": new_refresh_token}
