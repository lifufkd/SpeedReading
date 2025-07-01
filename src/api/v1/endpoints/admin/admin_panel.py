from fastapi import APIRouter, status, Depends, Body, Path

from src.services.users.admin_panel import AdminPanelService
from src.dependencies.security import validate_token, validate_admin
from src.dependencies.services import get_admin_panel_service
from src.validators.users import validate_not_same_id
from src.core.jwt import get_password_hash
from src.dto.users.admin_panel import GetUserDTO, CreateUserDTO, UpdateUserDTO
from src.core.dto_to_schema import many_dto_to_schema, dto_to_schema
from src.schemas.users.admin_panel import UserSchema, CreateUserSchema, UpdateUserSchema

router = APIRouter(
    dependencies=[Depends(validate_token), Depends(validate_admin)],
)


@router.get("/users", status_code=status.HTTP_200_OK, response_model=list[UserSchema])
async def get_users(
        admin_panel_service: AdminPanelService = Depends(get_admin_panel_service),
):

    new_users = await admin_panel_service.get_all_users()
    new_users = await many_dto_to_schema(
        new_users,
        UserSchema
    )

    return new_users


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(
        request: CreateUserSchema = Body(),
        admin_panel_service: AdminPanelService = Depends(get_admin_panel_service),
):

    data = CreateUserDTO(
        password_hash=get_password_hash(password=request.password),
        **request.model_dump()
    )
    new_user = await admin_panel_service.create_user(user_name=request.login, data=data)
    new_user = await dto_to_schema(
        new_user,
        UserSchema
    )

    return new_user


@router.patch("/user/{user_id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def update_user(
        user_id: int = Path(),
        request: UpdateUserSchema = Body(),
        current_user: GetUserDTO = Depends(validate_token),
        admin_panel_service: AdminPanelService = Depends(get_admin_panel_service),
):
    await validate_not_same_id(user=current_user, user_id=user_id)

    data = UpdateUserDTO(
        password_hash=get_password_hash(request.password) if request.password else None,
        **request.model_dump()
    )
    user = await admin_panel_service.users_service.update(user_id=user_id, data=data)
    user = await dto_to_schema(
        user,
        UserSchema
    )

    return user


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int = Path(),
        current_user: GetUserDTO = Depends(validate_token),
        admin_panel_service: AdminPanelService = Depends(get_admin_panel_service),
):
    await validate_not_same_id(user=current_user, user_id=user_id)

    await admin_panel_service.users_service.delete(user_id)



