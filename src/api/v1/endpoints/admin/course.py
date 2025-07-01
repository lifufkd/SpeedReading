from fastapi import APIRouter, status, Depends, Body, Path

from src.services.learning.course import CourseService
from src.services.learning.assignment import AssignmentService
from src.dependencies.security import validate_token, validate_admin
from src.dependencies.services import get_course_service, get_assignment_service
from src.dto.learning.courses import (
    CreateCoursesDTO,
    UpdateCoursesDTO,
    UpdateCoursesExerciseDTO,
    UpdateCoursesLessonsDTO
)
from src.core.dto_to_schema import many_dto_to_schema, dto_to_schema
from src.schemas.learning.courses import (
    CoursesSchema,
    CoursesNestedSchema,
    CreateCoursesSchema,
    UpdateCoursesSchema,
    UpdateCoursesExerciseSchema,
    UpdateCoursesLessonsSchema
)

router = APIRouter(
    dependencies=[Depends(validate_token), Depends(validate_admin)],
)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[CoursesNestedSchema])
async def get_courses(
        course_service: CourseService = Depends(get_course_service)
):

    courses = await course_service.get_all()
    courses = await many_dto_to_schema(
        courses,
        CoursesNestedSchema
    )

    return courses


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CoursesSchema)
async def create_course(
        request: CreateCoursesSchema = Body(),
        course_service: CourseService = Depends(get_course_service)
):
    data = CreateCoursesDTO(
        **request.model_dump()
    )
    new_course = await course_service.create(data)
    new_course = await dto_to_schema(
        new_course,
        CoursesSchema
    )

    return new_course


@router.patch("/{course_id}", status_code=status.HTTP_200_OK, response_model=CoursesSchema)
async def update_course(
        course_id: int = Path(),
        request: UpdateCoursesSchema = Body(),
        course_service: CourseService = Depends(get_course_service)
):
    data = UpdateCoursesDTO(
        **request.model_dump()
    )
    course = await course_service.update(course_id, data)
    course = await dto_to_schema(
        course,
        CoursesSchema
    )

    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
        course_id: int = Path(),
        course_service: CourseService = Depends(get_course_service)
):
    await course_service.delete(course_id)


@router.patch("/{course_id}/exercises", status_code=status.HTTP_200_OK, response_model=CoursesNestedSchema)
async def update_course_exercises(
        course_id: int = Path(),
        request: UpdateCoursesExerciseSchema = Body(),
        course_service: CourseService = Depends(get_course_service),
        assignment_service: AssignmentService = Depends(get_assignment_service)
):
    data = UpdateCoursesExerciseDTO(
        **request.model_dump()
    )
    course = await course_service.update_exercises(course_id, data)
    await assignment_service.update_progress()
    course = await dto_to_schema(
        course,
        CoursesNestedSchema
    )

    return course


@router.patch("/{course_id}/lessons", status_code=status.HTTP_200_OK, response_model=CoursesNestedSchema)
async def update_course_lessons(
        course_id: int = Path(),
        request: UpdateCoursesLessonsSchema = Body(),
        course_service: CourseService = Depends(get_course_service),
        assignment_service: AssignmentService = Depends(get_assignment_service)
):
    data = UpdateCoursesLessonsDTO(
        **request.model_dump()
    )
    course = await course_service.update_lessons(course_id, data)
    await assignment_service.update_progress()
    course = await dto_to_schema(
        course,
        CoursesNestedSchema
    )

    return course
