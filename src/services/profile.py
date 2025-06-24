from src.uow.abstract import AbstractUoW
from src.core.jwt import get_password_hash
from src.schemas.users import GetUserSchema, UpdateUserSchema, UpdateUserDTO, CreateUserDTO
from src.core.exceptions import UserAlreadyExists, UserNotFound
from src.schemas.users import CreateUserSchema
from src.services.users_service import UsersService
from src.schemas.profile import UpdateProfileSchema, UpdateProfileDTO


class ProfileService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow
        self.users_service = UsersService(uow)
