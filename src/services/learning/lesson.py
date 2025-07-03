from src.services.learning.helper import LearningHelper
from src.uow.abstract import AbstractUoW
from src.core.exceptions import LessonsNotFound, ExerciseNotFound
from src.core.orm_to_dto import many_sqlalchemy_to_pydantic
from src.core.orm_to_dto import sqlalchemy_to_pydantic
from src.dto.learning.assignment import FilterUsersTasksDTO
from src.dto.learning.lessons import (
    GetLessonsDTO,
    GetNestedLessonsDTO,
    UpdateLessonRelationDTO,
    UpdateLessonsDTO,
    CreateLessonsDTO
)
from src.schemas.enums import TaskTypes


class LessonService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow
        self.learning_helper = LearningHelper()

    async def get_by_id(self, lesson_id: int) -> GetLessonsDTO:
        async with self.uow as uow:
            lesson = await uow.lesson_repository.get_by_id(lesson_id)
            if not lesson:
                raise LessonsNotFound()

            lesson = await sqlalchemy_to_pydantic(
                lesson,
                GetLessonsDTO
            )

            return lesson

    async def get_all(self) -> list[GetNestedLessonsDTO]:
        async with self.uow as uow:
            lessons = await uow.lesson_repository.get_all()
            lessons = await many_sqlalchemy_to_pydantic(
                lessons,
                GetNestedLessonsDTO
            )

            return lessons

    async def update_exercises(self, lesson_id: int, data: UpdateLessonRelationDTO) -> GetNestedLessonsDTO:
        async with self.uow as uow:
            lesson = await uow.lesson_repository.get_by_id(lesson_id)
            if not lesson:
                raise LessonsNotFound()

            await self.learning_helper.update_relation(
                entity=lesson,
                add_ids=data.add_ids,
                delete_ids=data.delete_ids,
                get_related=lambda l: l.exercises,
                id_getter=lambda e: e.exercise_id,
                repo_get_by_ids=uow.exercise_repository.get_by_ids,
                exception=ExerciseNotFound,
                uow=uow,
            )

            lesson = await sqlalchemy_to_pydantic(
                lesson,
                GetNestedLessonsDTO
            )

            return lesson

    async def create(self, data: CreateLessonsDTO) -> GetLessonsDTO:
        async with self.uow as uow:
            new_lesson = await uow.lesson_repository.add(data)
            new_lesson = await sqlalchemy_to_pydantic(
                new_lesson,
                GetLessonsDTO
            )

            return new_lesson

    async def update(self, lesson_id: int, data: UpdateLessonsDTO) -> GetLessonsDTO:
        async with self.uow as uow:
            lesson = await uow.lesson_repository.update(lesson_id, data)
            if not lesson:
                raise LessonsNotFound()

            lesson = await sqlalchemy_to_pydantic(
                lesson,
                GetLessonsDTO
            )
            return lesson

    async def delete(self, lesson_id: int) -> None:
        async with self.uow as uow:
            lesson = await uow.lesson_repository.delete(lesson_id)
            if not lesson:
                raise LessonsNotFound()

            data = FilterUsersTasksDTO(
                task_id=lesson_id,
                task_type=TaskTypes.LESSON
            )
            await uow.users_tasks_repository.delete(data)
