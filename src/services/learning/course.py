from src.services.learning.helper import LearningHelper
from src.uow.abstract import AbstractUoW
from src.core.exceptions import CoursesNotFound, ExerciseNotFound, LessonsNotFound
from src.core.orm_to_dto import many_sqlalchemy_to_pydantic
from src.core.orm_to_dto import sqlalchemy_to_pydantic
from src.dto.learning.assignment import FilterUsersTasksDTO
from src.dto.learning.courses import (
    GetCoursesDTO,
    GetNestedCoursesDTO,
    CreateCoursesDTO,
    UpdateCoursesDTO,
    UpdateCourseRelationDTO
)
from src.schemas.enums import TaskTypes


class CourseService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow
        self.learning_helper = LearningHelper()

    async def get_by_id(self, course_id: int) -> GetCoursesDTO:
        async with self.uow as uow:
            course = await uow.course_repository.get_by_id(course_id)
            if not course:
                raise CoursesNotFound()

            course = await sqlalchemy_to_pydantic(
                course,
                GetCoursesDTO
            )

            return course

    async def get_all(self) -> list[GetNestedCoursesDTO]:
        async with self.uow as uow:
            courses = await uow.course_repository.get_all()
            courses = await many_sqlalchemy_to_pydantic(
                courses,
                GetNestedCoursesDTO
            )

            return courses

    async def update_exercises(self, course_id: int, data: UpdateCourseRelationDTO) -> GetNestedCoursesDTO:
        async with self.uow as uow:
            course = await uow.course_repository.get_by_id(course_id)
            if not course:
                raise CoursesNotFound()

            await self.learning_helper.update_relation(
                entity=course,
                add_ids=data.add_ids,
                delete_ids=data.delete_ids,
                get_related=lambda c: c.exercises,
                id_getter=lambda e: e.exercise_id,
                repo_get_by_ids=uow.exercise_repository.get_by_ids,
                exception=ExerciseNotFound,
                uow=uow,
            )

            course = await sqlalchemy_to_pydantic(
                course,
                GetNestedCoursesDTO
            )

            return course

    async def update_lessons(self, course_id: int, data: UpdateCourseRelationDTO) -> GetNestedCoursesDTO:
        async with self.uow as uow:
            course = await uow.course_repository.get_by_id(course_id)
            if not course:
                raise CoursesNotFound()

            await self.learning_helper.update_relation(
                entity=course,
                add_ids=data.add_ids,
                delete_ids=data.delete_ids,
                get_related=lambda c: c.lessons,
                id_getter=lambda l: l.lesson_id,
                repo_get_by_ids=uow.lesson_repository.get_by_ids,
                exception=LessonsNotFound,
                uow=uow,
            )

            course = await sqlalchemy_to_pydantic(
                course,
                GetNestedCoursesDTO
            )

            return course

    async def create(self, data: CreateCoursesDTO) -> GetCoursesDTO:
        async with self.uow as uow:
            new_course = await uow.course_repository.add(data)
            new_course = await sqlalchemy_to_pydantic(
                new_course,
                GetCoursesDTO
            )

            return new_course

    async def update(self, course_id: int, data: UpdateCoursesDTO) -> GetCoursesDTO:
        async with self.uow as uow:
            course = await uow.course_repository.update(course_id, data)
            if not course:
                raise CoursesNotFound()

            course = await sqlalchemy_to_pydantic(
                course,
                GetCoursesDTO
            )
            return course

    async def delete(self, course_id: int) -> None:
        async with self.uow as uow:
            course = await uow.course_repository.delete(course_id)
            if not course:
                raise CoursesNotFound()

            data = FilterUsersTasksDTO(
                task_id=course_id,
                task_type=TaskTypes.COURSE
            )
            await uow.users_tasks_repository.delete(data)
