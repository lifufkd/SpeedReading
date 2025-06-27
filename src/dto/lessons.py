from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GetLessonsDTO(BaseModel):
    lesson_id: int
    title: str
    created_at: datetime
    updated_at: datetime


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

