from fastapi import APIRouter, status, Depends, Body, Path

from src.services.learning.assignment import AssignmentService
from src.dependencies.security import validate_token, validate_admin
from src.dependencies.services import get_assignment_service
from src.dto.learning.assignment import (
    UpdateAssignedExercisesDTO,
    UpdateAssignedLessonsDTO,
    UpdateAssignedCoursesDTO
)
from src.core.dto_to_schema import many_dto_to_schema, dto_to_schema
from src.schemas.users.assignments import (
    UserNestedTasksSchema,
    UserNestedSchema
)
from src.schemas.learning.assignment import (
    UpdateAssignedExercisesSchema,
    UpdateAssignedLessonsSchema,
    UpdateAssignedCoursesSchema
)

router = APIRouter(
    dependencies=[Depends(validate_token), Depends(validate_admin)],
)


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


@router.patch("/{user_id}/assignments/exercises", response_model=UserNestedTasksSchema, status_code=status.HTTP_200_OK)
async def update_assigned_exercises(
        user_id: int = Path(),
        request: UpdateAssignedExercisesSchema = Body(),
        assignment_service: AssignmentService = Depends(get_assignment_service),
):
    data = UpdateAssignedExercisesDTO(
        **request.model_dump(),
    )
    user = await assignment_service.update_exercise(user_id, data)
    await assignment_service.update_progress_by_user_id(user_id=user_id)
    user = await dto_to_schema(
        user,
        UserNestedTasksSchema
    )

    return user


@router.patch("/{user_id}/assignments/lessons", response_model=UserNestedTasksSchema, status_code=status.HTTP_200_OK)
async def update_assigned_lessons(
        user_id: int = Path(),
        request: UpdateAssignedLessonsSchema = Body(),
        assignment_service: AssignmentService = Depends(get_assignment_service),
):
    data = UpdateAssignedLessonsDTO(
        **request.model_dump(),
    )
    user = await assignment_service.update_lessons(user_id, data)
    await assignment_service.update_progress_by_user_id(user_id=user_id)
    user = await dto_to_schema(
        user,
        UserNestedTasksSchema
    )

    return user


@router.patch("/{user_id}/assignments/courses", response_model=UserNestedTasksSchema, status_code=status.HTTP_200_OK)
async def update_assigned_courses(
        user_id: int = Path(),
        request: UpdateAssignedCoursesSchema = Body(),
        assignment_service: AssignmentService = Depends(get_assignment_service)
):
    data = UpdateAssignedCoursesDTO(
        **request.model_dump(),
    )
    user = await assignment_service.update_courses(user_id, data)
    await assignment_service.update_progress_by_user_id(user_id=user_id)
    user = await dto_to_schema(
        user,
        UserNestedTasksSchema
    )

    return user
