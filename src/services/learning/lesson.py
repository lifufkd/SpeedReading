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

    async def get_by_ids(self, lessons_ids: list[int]) -> list[GetLessonsDTO] | None:
        async with self.uow as uow:
            lessons = await uow.lesson_repository.get_by_ids(lessons_ids)
            if not lessons:
                return None

            lessons = await many_sqlalchemy_to_pydantic(
                lessons,
                GetLessonsDTO
            )

            return lessons

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

            exercises = await uow.exercise_repository.get_by_ids(data.add_exercises_ids + data.delete_exercises_ids)
            if not exercises:
                raise ExerciseNotFound(data.add_exercises_ids + data.delete_exercises_ids)
            founded_exercises_ids = {exercise.exercise_id for exercise in exercises}
            missing_exercises_ids = list(set(data.add_exercises_ids + data.delete_exercises_ids) - founded_exercises_ids)
            if missing_exercises_ids:
                raise ExerciseNotFound(missing_exercises_ids)

            for exercise in exercises:
                if exercise.exercise_id in data.add_exercises_ids:
                    lesson.exercises.append(exercise)
                elif exercise.exercise_id in data.delete_exercises_ids:
                    lesson.exercises.remove(exercise)

            uow.flush()

            exercise = await sqlalchemy_to_pydantic(
                exercise,
                GetNestedLessonsDTO
            )

            return exercise

    async def update_courses(self, lesson_id: int, data: UpdateLessonsCoursesDTO) -> GetNestedLessonsDTO:
        async with self.uow as uow:
            lesson = await uow.lesson_repository.get_by_id(lesson_id)
            if not lesson:
                raise LessonsNotFound()

            courses = await uow.course_repository.get_by_ids(data.add_courses_ids + data.delete_courses_ids)
            founded_courses_ids = {course.course_id for course in courses}
            missing_courses_ids = list(set(data.add_courses_ids + data.delete_courses_ids) - founded_courses_ids)
            if missing_courses_ids:
                raise CoursesNotFound(missing_courses_ids)

            for course in courses:
                if course.course_id in data.add_courses_ids:
                    lesson.courses.append(course)
                elif course.course_id in data.delete_courses_ids:
                    lesson.courses.remove(course)

            uow.flush()

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
