from fastapi import APIRouter, status, Depends, Body, Path

from src.schemas.enums import TaskTypes
from src.services.learning.assignment import AssignmentService
from src.dependencies.services import get_assignment_service
from src.dto.learning.assignment import UpdateAssignedTasksDTO
from src.core.exceptions import TaskTypeNotSupported
from src.core.dto_to_schema import many_dto_to_schema, dto_to_schema
from src.schemas.users.assignments import (
    UserNestedTasksSchema,
    UserNestedSchema
)
from src.schemas.learning.assignment import UpdateTaskRelationSchemaBase

router = APIRouter()


@router.get("/assignments", response_model=list[UserNestedSchema], status_code=status.HTTP_200_OK)
async def get_users(
        assignment_service: AssignmentService = Depends(get_assignment_service),
):

    users = await assignment_service.get_all_students()
    users = await many_dto_to_schema(
        users,
        UserNestedSchema
    )

    return users


@router.patch("/{user_id}/assignments", response_model=UserNestedTasksSchema, status_code=status.HTTP_200_OK)
async def update_assigned(
        user_id: int = Path(),
        request: UpdateTaskRelationSchemaBase = Body(),
        assignment_service: AssignmentService = Depends(get_assignment_service)
):
    data = UpdateAssignedTasksDTO(
        **request.model_dump(),
    )
    match data.type:
        case TaskTypes.EXERCISE:
            task = await assignment_service.update_exercises(user_id, data)
        case TaskTypes.LESSON:
            task = await assignment_service.update_lessons(user_id, data)
        case TaskTypes.COURSE:
            task = await assignment_service.update_courses(user_id, data)
        case _:
            raise TaskTypeNotSupported()

    await assignment_service.update_progress_by_user_id(user_id=user_id)
    task = await dto_to_schema(
        task,
        UserNestedTasksSchema
    )

    return task
