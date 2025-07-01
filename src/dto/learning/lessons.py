from pydantic import BaseModel
from typing import Optional

from src.dto.base import TimestampedDTO


class GetLessonsDTO(TimestampedDTO):
    lesson_id: int
    title: str


class GetLessonNestedExercisesDTO(GetLessonsDTO):
    exercises: list["GetExercisesDTO"]


class GetNestedLessonsDTO(GetLessonsDTO):
    exercises: list["GetExercisesDTO"]
    courses: list["GetCoursesDTO"]


class CreateLessonsDTO(BaseModel):
    title: str


class UpdateLessonsDTO(BaseModel):
    title: Optional[str] = None


class UpdateLessonsExerciseDTO(BaseModel):
    add_exercises_ids: list[int]
    delete_exercises_ids: list[int]


class UpdateLessonsCoursesDTO(BaseModel):
    add_courses_ids: list[int]
    delete_courses_ids: list[int]

