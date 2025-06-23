from src.schemas.enums import UsersRoles
from src.core.exceptions import UserIsNotAdmin
from src.schemas.users import UserSchema


async def validate_admin(user: UserSchema) -> None:
    if user.role != UsersRoles.ADMIN:
        raise UserIsNotAdmin()
