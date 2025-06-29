from functools import partial

from src.uow.abstract import AbstractUoW
from src.core.exceptions import CoursesNotFound, ExerciseNotFound, LessonsNotFound
from src.core.orm_to_dto import many_sqlalchemy_to_pydantic
from src.core.orm_to_dto import sqlalchemy_to_pydantic
from src.dto.courses import (
    GetCoursesDTO,
    GetNestedCoursesDTO,
    CreateCoursesDTO,
    UpdateCoursesDTO,
    UpdateCoursesExerciseDTO,
    UpdateCoursesLessonsDTO
)
from src.validators.common import is_number_in_list, is_number_not_in_list
from src.services.utils.validate_all_ids_found import validate_all_ids_found


class CourseService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

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

    async def update_exercises(self, course_id: int, data: UpdateCoursesExerciseDTO) -> GetNestedCoursesDTO:
        async with self.uow as uow:
            course = await uow.course_repository.get_by_id(course_id)
            if not course:
                raise CoursesNotFound()
            existed_exercises_ids = [exercise.exercise_id for exercise in course.exercises]

            exercises = await uow.exercise_repository.get_by_ids(data.add_exercises_ids + data.delete_exercises_ids)
            validate_all_ids_found(
                input_ids=data.add_exercises_ids + data.delete_exercises_ids,
                founded_objects=exercises,
                id_getter_function=lambda exercise: exercise.exercise_id,
                exception_builder=ExerciseNotFound
            )

            data.add_exercises_ids = list(
                filter(partial(is_number_not_in_list, list_=existed_exercises_ids), data.add_exercises_ids))
            data.delete_exercises_ids = list(
                filter(partial(is_number_in_list, list_=existed_exercises_ids), data.delete_exercises_ids))

            for exercise in exercises:
                if exercise.exercise_id in data.add_exercises_ids:
                    course.exercises.append(exercise)
                elif exercise.exercise_id in data.delete_exercises_ids:
                    course.exercises.remove(exercise)

            await uow.flush()

            course = await sqlalchemy_to_pydantic(
                course,
                GetNestedCoursesDTO
            )

            return course

    async def update_lessons(self, course_id: int, data: UpdateCoursesLessonsDTO) -> GetNestedCoursesDTO:
        async with self.uow as uow:
            course = await uow.course_repository.get_by_id(course_id)
            if not course:
                raise CoursesNotFound()
            existed_lessons_ids = [lesson.lesson_id for lesson in course.lessons]

            lessons = await uow.lesson_repository.get_by_ids(data.add_lessons_ids + data.delete_lessons_ids)
            validate_all_ids_found(
                input_ids=data.add_lessons_ids + data.delete_lessons_ids,
                founded_objects=lessons,
                id_getter_function=lambda lesson: lesson.lesson_id,
                exception_builder=LessonsNotFound
            )

            data.add_lessons_ids = list(
                filter(partial(is_number_not_in_list, list_=existed_lessons_ids), data.add_lessons_ids))
            data.delete_lessons_ids = list(
                filter(partial(is_number_in_list, list_=existed_lessons_ids), data.delete_lessons_ids))

            for lesson in lessons:
                if lesson.lesson_id in data.add_lessons_ids:
                    course.lessons.append(lesson)
                elif lesson.lesson_id in data.delete_lessons_ids:
                    course.lessons.remove(lesson)

            await uow.flush()

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
