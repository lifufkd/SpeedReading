from fastapi import APIRouter, status, Depends, Body, Path

from src.core.exceptions import TaskTypeNotSupported
from src.services.learning.lesson import LessonService
from src.services.learning.assignment import AssignmentService
from src.dependencies.services import get_lesson_service, get_assignment_service
from src.dto.learning.lessons import (
    CreateLessonsDTO,
    UpdateLessonsDTO,
    UpdateLessonRelationDTO
)
from src.core.dto_to_schema import many_dto_to_schema, dto_to_schema
from src.schemas.enums import TaskTypes
from src.schemas.learning.lessons import (
    LessonsNestedSchema,
    LessonsSchema,
    CreateLessonsSchema,
    UpdateLessonsSchema,
    UpdateLessonRelationSchema
)

router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=list[LessonsNestedSchema])
async def get_lessons(
        lesson_service: LessonService = Depends(get_lesson_service)
):

    lessons = await lesson_service.get_all()
    lessons = await many_dto_to_schema(
        lessons,
        LessonsNestedSchema
    )

    return lessons


@router.post("", status_code=status.HTTP_201_CREATED, response_model=LessonsSchema)
async def create_lesson(
        request: CreateLessonsSchema = Body(),
        lesson_service: LessonService = Depends(get_lesson_service)
):
    data = CreateLessonsDTO(
        **request.model_dump()
    )
    new_lesson = await lesson_service.create(data)
    new_lesson = await dto_to_schema(
        new_lesson,
        LessonsSchema
    )

    return new_lesson


@router.patch("/{lesson_id}", status_code=status.HTTP_200_OK, response_model=LessonsSchema)
async def update_lesson(
        lesson_id: int = Path(),
        request: UpdateLessonsSchema = Body(),
        lesson_service: LessonService = Depends(get_lesson_service)
):
    data = UpdateLessonsDTO(
        **request.model_dump()
    )
    lesson = await lesson_service.update(lesson_id, data)
    lesson = await dto_to_schema(
        lesson,
        LessonsSchema
    )

    return lesson


@router.delete("/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(
        lesson_id: int = Path(),
        lesson_service: LessonService = Depends(get_lesson_service)
):
    await lesson_service.delete(lesson_id)


@router.patch("/{lesson_id}/tasks", status_code=status.HTTP_200_OK, response_model=LessonsNestedSchema)
async def update_lesson_tasks(
        lesson_id: int = Path(),
        request: UpdateLessonRelationSchema = Body(),
        lesson_service: LessonService = Depends(get_lesson_service),
        assignment_service: AssignmentService = Depends(get_assignment_service)
):
    data = UpdateLessonRelationDTO(
        **request.model_dump()
    )
    match data.type:
        case TaskTypes.EXERCISE:
            task = await lesson_service.update_exercises(lesson_id, data)
        case _:
            raise TaskTypeNotSupported()

    await assignment_service.update_progress()
    task = await dto_to_schema(
        task,
        LessonsNestedSchema
    )

    return task
