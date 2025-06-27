from src.uow.abstract import AbstractUoW
from src.core.exceptions import ExerciseNotFound, LessonsNotFound, CoursesNotFound
from src.core.orm_to_dto import many_sqlalchemy_to_pydantic
from src.core.orm_to_dto import sqlalchemy_to_pydantic
from src.dto.exercises import (
    GetExercisesDTO,
    GetNestedExercisesDTO,
    CreateExerciseDTO,
    UpdateExerciseDTO,
    UpdateExerciseLessonsDTO,
    UpdateExerciseCoursesDTO
)


class ExerciseService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def get_by_id(self, exercise_id: int) -> GetExercisesDTO:
        async with self.uow as uow:
            exercise = await uow.exercise_repository.get_by_id(exercise_id)
            if not exercise:
                raise ExerciseNotFound()

            exercise = await sqlalchemy_to_pydantic(
                exercise,
                GetExercisesDTO
            )

            return exercise

    async def get_by_ids(self, exercises_ids: list[int]) -> list[GetExercisesDTO] | None:
        async with self.uow as uow:
            exercises = await uow.exercise_repository.get_by_ids(exercises_ids)
            if not exercises:
                return None

            exercises = await many_sqlalchemy_to_pydantic(
                exercises,
                GetExercisesDTO
            )

            return exercises

    async def get_all(self) -> list[GetNestedExercisesDTO]:
        async with self.uow as uow:
            exercises = await uow.exercise_repository.get_all()
            exercises = await many_sqlalchemy_to_pydantic(
                exercises,
                GetNestedExercisesDTO
            )

            return exercises

    async def update_lessons(self, exercise_id: int, data: UpdateExerciseLessonsDTO) -> GetNestedExercisesDTO:
        async with self.uow as uow:
            exercise = await uow.exercise_repository.get_by_id(exercise_id)
            if not exercise:
                raise ExerciseNotFound()

            lessons = await uow.lesson_repository.get_by_ids(data.add_lessons_ids + data.delete_lessons_ids)
            if not lessons:
                raise LessonsNotFound(data.add_lessons_ids + data.delete_lessons_ids)
            founded_lessons_ids = {lesson.lesson_id for lesson in lessons}
            missing_lessons_ids = list(set(data.add_lessons_ids + data.delete_lessons_ids) - founded_lessons_ids)
            if missing_lessons_ids:
                raise LessonsNotFound(missing_lessons_ids)

            for lesson in lessons:
                if lesson.lesson_id in data.add_lessons_ids:
                    exercise.lessons.append(lesson)
                elif lesson.lesson_id in data.delete_lessons_ids:
                    exercise.lessons.remove(lesson)

            uow.flush()

            exercise = await sqlalchemy_to_pydantic(
                exercise,
                GetNestedExercisesDTO
            )

            return exercise

    async def update_courses(self, exercise_id: int, data: UpdateExerciseCoursesDTO) -> GetNestedExercisesDTO:
        async with self.uow as uow:
            exercise = await uow.exercise_repository.get_by_id(exercise_id)
            if not exercise:
                raise ExerciseNotFound()

            courses = await uow.course_repository.get_by_ids(data.add_courses_ids + data.delete_courses_ids)
            founded_courses_ids = {course.course_id for course in courses}
            missing_courses_ids = list(set(data.add_courses_ids + data.delete_courses_ids) - founded_courses_ids)
            if missing_courses_ids:
                raise CoursesNotFound(missing_courses_ids)

            for course in courses:
                if course.course_id in data.add_courses_ids:
                    exercise.courses.append(course)
                elif course.course_id in data.delete_courses_ids:
                    exercise.courses.remove(course)

            uow.flush()

            exercise = await sqlalchemy_to_pydantic(
                exercise,
                GetNestedExercisesDTO
            )

            return exercise

    async def create(self, data: CreateExerciseDTO) -> GetExercisesDTO:
        async with self.uow as uow:
            new_exercise = await uow.exercise_repository.add(data)
            new_exercise = await sqlalchemy_to_pydantic(
                new_exercise,
                GetExercisesDTO
            )

            return new_exercise

    async def update(self, exercise_id: int, data: UpdateExerciseDTO) -> GetExercisesDTO:
        async with self.uow as uow:
            exercise = await uow.exercise_repository.update(exercise_id, data)
            if not exercise:
                raise ExerciseNotFound()

            exercise = await sqlalchemy_to_pydantic(
                exercise,
                GetExercisesDTO
            )
            return exercise

    async def delete(self, exercise_id: int) -> None:
        async with self.uow as uow:
            exercise = await uow.exercise_repository.delete(exercise_id)
            if not exercise:
                raise ExerciseNotFound()
