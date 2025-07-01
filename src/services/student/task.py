from src.uow.abstract import AbstractUoW
from src.core.exceptions import UserNotFound
from src.validators.users import validate_user_is_student
from src.schemas.enums import TaskTypes
from src.dto.student.tasks import GetUserTaskTreeDTO
from src.dto.learning.exercises import GetExercisesDTO
from src.dto.learning.lessons import GetLessonNestedExercisesDTO
from src.dto.learning.courses import GetCourseFullNestedDTO
from src.core.orm_to_dto import sqlalchemy_to_pydantic


class TasksService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def get(self, user_id: int) -> GetUserTaskTreeDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)   # TODO: User must be as DTO object

            user_tasks_tree = GetUserTaskTreeDTO()
            for task in user.tasks:
                match task.task_type:
                    case TaskTypes.EXERCISE:
                        exercise = await uow.exercise_repository.get_by_id(task.task_id)
                        exercise_dto = await sqlalchemy_to_pydantic(
                            exercise,
                            GetExercisesDTO
                        )
                        user_tasks_tree.exercises.append(exercise_dto)
                    case TaskTypes.LESSON:
                        lesson = await uow.lesson_repository.get_by_id(task.task_id)
                        lesson_dto = await sqlalchemy_to_pydantic(
                            lesson,
                            GetLessonNestedExercisesDTO
                        )
                        user_tasks_tree.lessons.append(lesson_dto)
                    case TaskTypes.COURSE:
                        course = await uow.course_repository.get_by_id(task.task_id)
                        course_dto = await sqlalchemy_to_pydantic(
                            course,
                            GetCourseFullNestedDTO
                        )
                        user_tasks_tree.courses.append(course_dto)

            return user_tasks_tree



