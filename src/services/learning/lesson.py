from functools import partial

from src.uow.abstract import AbstractUoW
from src.core.exceptions import LessonsNotFound, ExerciseNotFound, CoursesNotFound
from src.core.orm_to_dto import many_sqlalchemy_to_pydantic
from src.core.orm_to_dto import sqlalchemy_to_pydantic
from src.dto.lessons import (
    GetLessonsDTO,
    GetNestedLessonsDTO,
    UpdateLessonsCoursesDTO,
    UpdateLessonsExerciseDTO,
    UpdateLessonsDTO,
    CreateLessonsDTO
)
from src.validators.common import is_number_in_list, is_number_not_in_list


class LessonService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

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

    async def update_exercises(self, lesson_id: int, data: UpdateLessonsExerciseDTO) -> GetNestedLessonsDTO:
        async with self.uow as uow:
            lesson = await uow.lesson_repository.get_by_id(lesson_id)
            if not lesson:
                raise LessonsNotFound()
            existed_exercises_ids = [exercise.exercise_id for exercise in lesson.exercises]

            exercises = await uow.exercise_repository.get_by_ids(data.add_exercises_ids + data.delete_exercises_ids)
            if not exercises:
                raise ExerciseNotFound(data.add_exercises_ids + data.delete_exercises_ids)
            founded_exercises_ids = {exercise.exercise_id for exercise in exercises}
            missing_exercises_ids = list(set(data.add_exercises_ids + data.delete_exercises_ids) - founded_exercises_ids)
            if missing_exercises_ids:
                raise ExerciseNotFound(missing_exercises_ids)

            data.add_exercises_ids = list(
                filter(partial(is_number_not_in_list, list_=existed_exercises_ids), data.add_exercises_ids))
            data.delete_exercises_ids = list(
                filter(partial(is_number_in_list, list_=existed_exercises_ids), data.delete_exercises_ids))

            for exercise in exercises:
                if exercise.exercise_id in data.add_exercises_ids:
                    lesson.exercises.append(exercise)
                elif exercise.exercise_id in data.delete_exercises_ids:
                    lesson.exercises.remove(exercise)

            await uow.flush()

            lesson = await sqlalchemy_to_pydantic(
                lesson,
                GetNestedLessonsDTO
            )

            return lesson

    async def update_courses(self, lesson_id: int, data: UpdateLessonsCoursesDTO) -> GetNestedLessonsDTO:
        async with self.uow as uow:
            lesson = await uow.lesson_repository.get_by_id(lesson_id)
            if not lesson:
                raise LessonsNotFound()
            existed_courses_ids = [course.course_id for course in lesson.courses]

            courses = await uow.course_repository.get_by_ids(data.add_courses_ids + data.delete_courses_ids)
            founded_courses_ids = {course.course_id for course in courses}
            missing_courses_ids = list(set(data.add_courses_ids + data.delete_courses_ids) - founded_courses_ids)
            if missing_courses_ids:
                raise CoursesNotFound(missing_courses_ids)

            data.add_courses_ids = list(
                filter(partial(is_number_not_in_list, list_=existed_courses_ids), data.add_courses_ids))
            data.delete_courses_ids = list(
                filter(partial(is_number_in_list, list_=existed_courses_ids), data.delete_courses_ids))

            for course in courses:
                if course.course_id in data.add_courses_ids:
                    lesson.courses.append(course)
                elif course.course_id in data.delete_courses_ids:
                    lesson.courses.remove(course)

            await uow.flush()

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
