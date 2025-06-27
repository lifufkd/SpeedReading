from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GetCoursesDTO(BaseModel):
    course_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class GetNestedCoursesDTO(GetCoursesDTO):
    lessons: list["GetLessonsDTO"]
    exercises: list["GetExercisesDTO"]


class CreateCoursesDTO(BaseModel):
    title: str


class UpdateCoursesDTO(BaseModel):
    title: Optional[str] = None


class UpdateCoursesExerciseDTO(BaseModel):
    add_exercises_ids: list[int]
    delete_exercises_ids: list[int]


class UpdateCoursesLessonsDTO(BaseModel):
    add_lessons_ids: list[int]
    delete_lessons_ids: list[int]
