from pydantic import BaseModel
from datetime import datetime

from src.schemas.enums import TaskTypes


class AssignmentDTO(BaseModel):
    users_tasks_id: int
    user_id: int
    task_id: int
    task_type: TaskTypes
    created_at: datetime
    updated_at: datetime


class UpdateAssignedExercisesDTO(BaseModel):
    add_exercises_ids: list[int]
    delete_exercises_ids: list[int]


class UpdateAssignedLessonsDTO(BaseModel):
    add_lessons_ids: list[int]
    delete_lessons_ids: list[int]


class UpdateAssignedCoursesDTO(BaseModel):
    add_courses_ids: list[int]
    delete_courses_ids: list[int]
