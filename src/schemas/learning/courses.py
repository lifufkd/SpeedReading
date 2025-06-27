from pydantic import BaseModel
from datetime import datetime


class CoursesSchema(BaseModel):
    course_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class CoursesNestedSchema(CoursesSchema):
    lessons: list["LessonsSchema"]
    exercises: list["ExerciseSchema"]
