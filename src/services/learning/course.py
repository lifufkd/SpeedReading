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

    async def get_by_ids(self, courses_ids: list[int]) -> list[GetCoursesDTO] | None:
        async with self.uow as uow:
            courses = await uow.course_repository.get_by_ids(courses_ids)
            if not courses:
                return None

            courses = await many_sqlalchemy_to_pydantic(
                courses,
                GetCoursesDTO
            )

            return courses

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

            exercises = await uow.exercise_repository.get_by_ids(data.add_exercises_ids + data.delete_exercises_ids)
            if not exercises:
                raise ExerciseNotFound(data.add_exercises_ids + data.delete_exercises_ids)
            founded_exercises_ids = {exercise.exercise_id for exercise in exercises}
            missing_exercises_ids = list(set(data.add_exercises_ids + data.delete_exercises_ids) - founded_exercises_ids)
            if missing_exercises_ids:
                raise ExerciseNotFound(missing_exercises_ids)

            for exercise in exercises:
                if exercise.exercise_id in data.add_exercises_ids:
                    course.exercises.append(exercise)
                elif exercise.exercise_id in data.delete_exercises_ids:
                    course.exercises.remove(exercise)

            uow.flush()

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

            lessons = await uow.lesson_repository.get_by_ids(data.add_lessons_ids + data.delete_lessons_ids)
            if not lessons:
                raise LessonsNotFound(data.add_lessons_ids + data.delete_lessons_ids)
            founded_lessons_ids = {lesson.lesson_id for lesson in lessons}
            missing_lessons_ids = list(set(data.add_lessons_ids + data.delete_lessons_ids) - founded_lessons_ids)
            if missing_lessons_ids:
                raise LessonsNotFound(missing_lessons_ids)

            for lesson in lessons:
                if lesson.lesson_id in data.add_lessons_ids:
                    course.lessons.append(lesson)
                elif lesson.lesson_id in data.delete_lessons_ids:
                    course.lessons.remove(lesson)

            uow.flush()

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
