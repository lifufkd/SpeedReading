from pydantic import BaseModel
from datetime import datetime

from src.schemas.enums import TaskTypes, ExerciseCompleteStatus
from src.schemas.learning.base import UniqueFieldValidator


class AssignmentSchema(BaseModel):
    users_tasks_id: int
    user_id: int
    task_id: int
    task_type: TaskTypes
    created_at: datetime
    updated_at: datetime


class UsersProgressSchema(BaseModel):
    user_id: int
    exercise_id: int
    status: ExerciseCompleteStatus
    created_at: datetime
    updated_at: datetime


class UpdateAssignedExercisesSchema(UniqueFieldValidator):
    add_exercises_ids: list[int]
    delete_exercises_ids: list[int]


class UpdateAssignedLessonsSchema(UniqueFieldValidator):
    add_lessons_ids: list[int]
    delete_lessons_ids: list[int]


class UpdateAssignedCoursesSchema(UniqueFieldValidator):
    add_courses_ids: list[int]
    delete_courses_ids: list[int]
