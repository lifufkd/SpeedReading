from src.schemas.users import UserSchema
from src.core.exceptions import UserIdIsSame


async def validate_not_same_id(user: UserSchema, user_id: int) -> None:
    if user.user_id == user_id:
        raise UserIdIsSame()
