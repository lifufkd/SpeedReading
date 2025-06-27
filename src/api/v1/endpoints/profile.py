from fastapi import APIRouter, status, Depends, Body

from src.dependencies.security import validate_token
from src.dependencies.services import get_profile_service
from src.services.profile import ProfileService
from src.schemas.users.profile import UpdateProfileSchema, UserSchema
from src.dto.users import GetUsersDTO, UpdateUsersDTO
from src.core.jwt import get_password_hash
from src.core.dto_to_schema import dto_to_schema


router = APIRouter()


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_my_profile(
        current_user: GetUsersDTO = Depends(validate_token)
):
    user = UserSchema(
        **current_user.model_dump()
    )
    return user


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def update_my_profile(
        request: UpdateProfileSchema = Body(),
        current_user: GetUsersDTO = Depends(validate_token),
        profile_service: ProfileService = Depends(get_profile_service)
):
    data = UpdateUsersDTO(
        password_hash=get_password_hash(request.password) if request.password else None,
        **request.model_dump()
    )
    user = await profile_service.users_service.update(user_id=current_user.user_id, data=data)
    user = await dto_to_schema(
        user,
        UserSchema
    )

    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_profile(
        current_user: GetUsersDTO = Depends(validate_token),
        profile_service: ProfileService = Depends(get_profile_service)
):
    await profile_service.users_service.delete(current_user.user_id)



