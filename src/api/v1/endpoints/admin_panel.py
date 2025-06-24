from fastapi import APIRouter, status, Depends, Body, Query

from src.services.admin_panel import AdminPanelService
from src.dependencies.security import validate_token
from src.dependencies.services import get_admin_panel_service
from src.schemas.users import CreateUserSchema, GetUserSchema, UserSchema, UpdateUserSchema
from src.validators.permissions import validate_admin
from src.validators.users import validate_not_same_id

router = APIRouter()


@router.get("/users", response_model=list[GetUserSchema], status_code=status.HTTP_200_OK)
async def get_users(
        current_user: UserSchema = Depends(validate_token),
        admin_panel_service: AdminPanelService = Depends(get_admin_panel_service),
):
    await validate_admin(user=current_user)

    new_user = await admin_panel_service.get_all_users()
    return new_user


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=GetUserSchema)
async def create_user(
        request: CreateUserSchema = Body(),
        current_user: UserSchema = Depends(validate_token),
        admin_panel_service: AdminPanelService = Depends(get_admin_panel_service),
):
    await validate_admin(user=current_user)

    new_user = await admin_panel_service.create_user(request)
    return new_user


@router.patch("/user", status_code=status.HTTP_200_OK, response_model=GetUserSchema)
async def update_user(
        request: UpdateUserSchema = Body(),
        current_user: UserSchema = Depends(validate_token),
        admin_panel_service: AdminPanelService = Depends(get_admin_panel_service),
):
    await validate_admin(user=current_user)
    await validate_not_same_id(user=current_user, user_id=request.user_id)

    user = await admin_panel_service.users_service.update_user(request)
    return user


@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int = Query(),
        current_user: UserSchema = Depends(validate_token),
        admin_panel_service: AdminPanelService = Depends(get_admin_panel_service),
):
    await validate_admin(user=current_user)
    await validate_not_same_id(user=current_user, user_id=user_id)

    await admin_panel_service.users_service.delete_user(user_id)



