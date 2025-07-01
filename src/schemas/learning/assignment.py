from src.schemas.enums import TaskTypes, ExerciseCompleteStatus
from src.schemas.learning.base import UniqueFieldValidator
from src.schemas.base import TimestampedSchema


class AssignmentSchema(TimestampedSchema):
    users_tasks_id: int
    user_id: int
    task_id: int
    task_type: TaskTypes


class UsersProgressSchema(TimestampedSchema):
    user_id: int
    exercise_id: int
    status: ExerciseCompleteStatus


class UpdateAssignedExercisesSchema(UniqueFieldValidator):
    add_exercises_ids: list[int]
    delete_exercises_ids: list[int]


class UpdateAssignedLessonsSchema(UniqueFieldValidator):
    add_lessons_ids: list[int]
    delete_lessons_ids: list[int]


class UpdateAssignedCoursesSchema(UniqueFieldValidator):
    add_courses_ids: list[int]
    delete_courses_ids: list[int]
