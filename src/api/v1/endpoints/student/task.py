from fastapi import APIRouter, status, Depends, Body, Path

from src.services.student.task import TasksService
from src.dependencies.security import validate_token
from src.dependencies.services import get_tasks_service
from src.dto.users import GetUsersDTO
from src.schemas.student.tasks import UserTaskTreeSchema
from src.core.dto_to_schema import dto_to_schema

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=UserTaskTreeSchema)
async def get_tasks(
        current_user: GetUsersDTO = Depends(validate_token),
        tasks_service: TasksService = Depends(get_tasks_service),
):

    tasks = await tasks_service.get(current_user.user_id)
    tasks = await dto_to_schema(
        tasks,
        UserTaskTreeSchema
    )
    return tasks
