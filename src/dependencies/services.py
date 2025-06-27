from fastapi import Depends

from src.services.exercise import ExerciseService
from src.services.auth import AuthService
from src.services.admin_panel import AdminPanelService
from src.services.profile import ProfileService
from src.uow.abstract import AbstractUoW
from src.dependencies.uow import get_uow


async def get_auth_service(uow: AbstractUoW = Depends(get_uow)):
    return AuthService(uow)


async def get_admin_panel_service(uow: AbstractUoW = Depends(get_uow)):
    return AdminPanelService(uow)


async def get_profile_service(uow: AbstractUoW = Depends(get_uow)):
    return ProfileService(uow)


async def get_exercise_service(uow: AbstractUoW = Depends(get_uow)):
    return ExerciseService(uow)
