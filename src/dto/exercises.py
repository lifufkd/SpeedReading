from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.schemas.enums import ExerciseTypes


class GetExercisesDTO(BaseModel):
    exercise_id: int
    title: str
    type: ExerciseTypes
    created_at: datetime
    updated_at: datetime


class GetNestedExercisesDTO(GetExercisesDTO):
    lessons: list["GetLessonsDTO"]
    courses: list["GetCoursesDTO"]


class CreateExerciseDTO(BaseModel):
    title: str
    type: ExerciseTypes


class UpdateExerciseDTO(BaseModel):
    title: Optional[str] = None
    type: Optional[ExerciseTypes] = None


class UpdateExerciseLessonsDTO(BaseModel):
    add_lessons_ids: list[int]
    delete_lessons_ids: list[int]


class UpdateExerciseCoursesDTO(BaseModel):
    add_courses_ids: list[int]
    delete_courses_ids: list[int]
