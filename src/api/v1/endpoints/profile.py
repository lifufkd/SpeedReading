from fastapi import APIRouter, status, Depends, Body, Query

from src.services.admin_panel import AdminPanelService
from src.dependencies.security import validate_token
from src.dependencies.services import get_admin_panel_service, get_profile_service
from src.schemas.users import CreateUserSchema, GetUserSchema, UserSchema, UpdateUserSchema
from src.validators.permissions import validate_admin
from src.validators.users import validate_not_same_id
from src.services.profile import ProfileService
from src.schemas.profile import UpdateProfileSchema


router = APIRouter()


@router.get("/me", response_model=GetUserSchema, status_code=status.HTTP_200_OK)
async def get_my_profile(
        current_user: UserSchema = Depends(validate_token)
):
    user = GetUserSchema(
        **current_user.model_dump()
    )
    return user


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=GetUserSchema)
async def update_my_profile(
        request: UpdateProfileSchema = Body(),
        current_user: UserSchema = Depends(validate_token),
        profile_service: ProfileService = Depends(get_profile_service)
):

    user = await profile_service.users_service.update_profile(request)
    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_profile(
        current_user: UserSchema = Depends(validate_token),
        profile_service: ProfileService = Depends(get_profile_service)
):
    await profile_service.users_service.delete_user(current_user.user_id)



