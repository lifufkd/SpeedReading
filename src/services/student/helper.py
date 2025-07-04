from src.models.users import Users
from src.schemas.enums import TaskTypes


class StudentHelper:
    def __init__(self):
        pass

    async def extract_exercise_ids_from_tasks(
        self,
        user: Users,
        uow,
    ) -> set[int]:
        exercise_ids: set[int] = set()
        user_tasks = user.tasks

        for task in user_tasks:
            match task.task_type:
                case TaskTypes.EXERCISE:
                    exercise_ids.add(task.task_id)

                case TaskTypes.LESSON:
                    lesson = await uow.lesson_repository.get_by_id_exercises_nested(task.task_id)
                    if not lesson:
                        continue
                    exercise_ids.update([e.exercise_id for e in lesson.exercises])

                case TaskTypes.COURSE:
                    course = await uow.course_repository.get_by_id_full_nested(task.task_id)
                    if not course:
                        continue
                    for lesson in course.lessons:
                        exercise_ids.update([e.exercise_id for e in lesson.exercises])
                    for exercise in course.exercises:
                        exercise_ids.add(exercise.exercise_id)

        return exercise_ids
