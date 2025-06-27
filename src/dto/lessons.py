from pydantic import BaseModel
from datetime import datetime


class GetLessonsDTO(BaseModel):
    lesson_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class GetNestedLessonsDTO(GetLessonsDTO):
    exercises: list["GetExercisesDTO"]
    courses: list["GetCoursesDTO"]
