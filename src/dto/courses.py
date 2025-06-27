from pydantic import BaseModel
from datetime import datetime


class GetCoursesDTO(BaseModel):
    course_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class GetNestedCoursesDTO(GetCoursesDTO):
    lessons: list["GetLessonsDTO"]
    exercises: list["GetExercisesDTO"]
