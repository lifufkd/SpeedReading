from src.dto.users import GetUsersDTO
from src.core.exceptions import UserIdIsSame, UserIsNotStudent
from src.schemas.enums import UsersRoles


async def validate_not_same_id(user: GetUsersDTO, user_id: int) -> None:
    if user.user_id == user_id:
        raise UserIdIsSame()


async def validate_user_is_student(user: GetUsersDTO) -> None:
    if user.role != UsersRoles.USER:
        raise UserIsNotStudent()
