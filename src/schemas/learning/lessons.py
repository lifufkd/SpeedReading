from pydantic import BaseModel
from datetime import datetime


class LessonsSchema(BaseModel):
    lesson_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class LessonsNestedSchema(LessonsSchema):
    exercises: list["ExerciseSchema"]
    courses: list["CoursesSchema"]
