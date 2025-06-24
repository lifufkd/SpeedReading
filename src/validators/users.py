from src.dto.users import GetUsersDTO
from src.core.exceptions import UserIdIsSame


async def validate_not_same_id(user: GetUsersDTO, user_id: int) -> None:
    if user.user_id == user_id:
        raise UserIdIsSame()
