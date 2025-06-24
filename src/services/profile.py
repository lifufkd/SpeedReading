from src.uow.abstract import AbstractUoW
from src.services.users import UsersService


class ProfileService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow
        self.users_service = UsersService(uow)
