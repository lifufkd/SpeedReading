from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.schemas.enums import TaskTypes
from src.schemas.enums import ExerciseCompleteStatus


class UsersTasksDTO(BaseModel):
    users_tasks_id: int
    user_id: int
    task_id: int
    task_type: TaskTypes
    created_at: datetime
    updated_at: datetime


class UsersProgressDTO(BaseModel):
    user_id: int
    exercise_id: int
    status: ExerciseCompleteStatus
    created_at: datetime
    updated_at: datetime


class FilterUsersTasksDTO(BaseModel):
    users_tasks_id: Optional[int] = None
    user_id: Optional[int] = None
    task_id: Optional[int] = None
    task_type: Optional[TaskTypes] = None


class UpdateAssignedExercisesDTO(BaseModel):
    add_exercises_ids: list[int]
    delete_exercises_ids: list[int]


class UpdateAssignedLessonsDTO(BaseModel):
    add_lessons_ids: list[int]
    delete_lessons_ids: list[int]


class UpdateAssignedCoursesDTO(BaseModel):
    add_courses_ids: list[int]
    delete_courses_ids: list[int]
