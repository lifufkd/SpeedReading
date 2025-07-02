from fastapi import APIRouter, status, Depends, Query, Body

from src.services.student.progress import ProgressService
from src.dependencies.security import validate_token
from src.dependencies.services import get_progress_service
from src.dto.users.auth import GetUserDTO
from src.dto.student.progresses import UpdateUserProgressDTO
from src.schemas.users.assignments import UserNestedProgressSchema
from src.schemas.student.progresses import UserProgressSchema, UpdateUserProgressSchema
from src.core.dto_to_schema import dto_to_schema

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=UserNestedProgressSchema)
async def get_progress(
        current_user: GetUserDTO = Depends(validate_token),
        progress_service: ProgressService = Depends(get_progress_service),
):

    tasks = await progress_service.get(current_user.user_id)
    tasks = await dto_to_schema(
        tasks,
        UserNestedProgressSchema
    )
    return tasks


@router.patch("", status_code=status.HTTP_200_OK, response_model=UserProgressSchema)
async def update_progress_status(
        exercise_id: int = Query(),
        request: UpdateUserProgressSchema = Body(),
        current_user: GetUserDTO = Depends(validate_token),
        progress_service: ProgressService = Depends(get_progress_service),
):
    data = UpdateUserProgressDTO(
        **request.model_dump(),
    )
    user_progress = await progress_service.update(current_user.user_id, exercise_id, data)

    user_progress = await dto_to_schema(
        user_progress,
        UserProgressSchema
    )

    return user_progress
