from src.uow.abstract import AbstractUoW
from src.core.exceptions import ExerciseNotFound, UserNotFound, LessonsNotFound, CoursesNotFound
from src.core.orm_to_dto import many_sqlalchemy_to_pydantic, sqlalchemy_to_pydantic
from src.dto.users import GetUserNestedTasksDTO, GetUserNestedProgressDTO, GetUserNestedDTO
from src.dto.learning.assignment import (
    UpdateAssignedExercisesDTO,
    UpdateAssignedLessonsDTO,
    UpdateAssignedCoursesDTO
)
from src.schemas.enums import TaskTypes
from src.models.users_tasks import UsersTasks
from src.models.m2m import UsersProgress
from src.models.users import Users
from src.validators.users import validate_user_is_student
from src.services.utils.validate_all_ids_found import validate_all_ids_found


class AssignmentService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def get_all_students(self) -> list[GetUserNestedDTO]:
        async with self.uow as uow:
            users = await uow.user_repository.get_all_students()
            users = await many_sqlalchemy_to_pydantic(
                users,
                GetUserNestedDTO
            )

            return users

    async def update_exercise(self, user_id: int, data: UpdateAssignedExercisesDTO) -> GetUserNestedTasksDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)   # TODO: User must be as DTO object

            exercises = await uow.exercise_repository.get_by_ids(data.add_exercises_ids + data.delete_exercises_ids)
            validate_all_ids_found(
                input_ids=data.add_exercises_ids + data.delete_exercises_ids,
                founded_objects=exercises,
                id_getter_function=lambda exercise: exercise.exercise_id,
                exception_builder=ExerciseNotFound
            )

            assigned_tasks = await uow.users_tasks_repository.get_by_task_type(user_id, TaskTypes.EXERCISE)
            if not assigned_tasks:
                assigned_exercises = []
            else:
                assigned_exercises = [assigned_task.task_id for assigned_task in assigned_tasks]

            for exercise_id in data.add_exercises_ids:
                if exercise_id in assigned_exercises:
                    continue
                task = UsersTasks(
                    task_id=exercise_id,
                    task_type=TaskTypes.EXERCISE
                )
                user.tasks.append(task)

            for assigned_task in assigned_tasks:
                if assigned_task.task_id in data.delete_exercises_ids:
                    user.tasks.remove(assigned_task)

            await uow.flush()

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserNestedTasksDTO
            )

            return user

    async def update_lessons(self, user_id: int, data: UpdateAssignedLessonsDTO) -> GetUserNestedTasksDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)  # TODO: User must be as DTO object

            lessons = await uow.lesson_repository.get_by_ids(data.add_lessons_ids + data.delete_lessons_ids)
            validate_all_ids_found(
                input_ids=data.add_lessons_ids + data.delete_lessons_ids,
                founded_objects=lessons,
                id_getter_function=lambda lesson: lesson.lesson_id,
                exception_builder=LessonsNotFound
            )

            assigned_tasks = await uow.users_tasks_repository.get_by_task_type(user_id, TaskTypes.LESSON)
            if not assigned_tasks:
                assigned_lessons = []
            else:
                assigned_lessons = [assigned_task.task_id for assigned_task in assigned_tasks]

            for lesson_id in data.add_lessons_ids:
                if lesson_id in assigned_lessons:
                    continue
                task = UsersTasks(
                    task_id=lesson_id,
                    task_type=TaskTypes.LESSON
                )
                user.tasks.append(task)

            for assigned_task in assigned_tasks:
                if assigned_task.task_id in data.delete_lessons_ids:
                    user.tasks.remove(assigned_task)

            await uow.flush()

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserNestedTasksDTO
            )

            return user

    async def update_courses(self, user_id: int, data: UpdateAssignedCoursesDTO) -> GetUserNestedTasksDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)  # TODO: User must be as DTO object

            courses = await uow.course_repository.get_by_ids(data.add_courses_ids + data.delete_courses_ids)
            validate_all_ids_found(
                input_ids=data.add_courses_ids + data.delete_courses_ids,
                founded_objects=courses,
                id_getter_function=lambda course: course.course_id,
                exception_builder=CoursesNotFound
            )

            assigned_tasks = await uow.users_tasks_repository.get_by_task_type(user_id, TaskTypes.COURSE)
            if not assigned_tasks:
                assigned_courses = []
            else:
                assigned_courses = [assigned_task.task_id for assigned_task in assigned_tasks]

            for course_id in data.add_courses_ids:
                if course_id in assigned_courses:
                    continue
                task = UsersTasks(
                    task_id=course_id,
                    task_type=TaskTypes.COURSE
                )
                user.tasks.append(task)

            for assigned_task in assigned_tasks:
                if assigned_task.task_id in data.delete_courses_ids:
                    user.tasks.remove(assigned_task)

            await uow.flush()

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserNestedTasksDTO
            )

            return user

    async def _update_students_progress(self, user: Users, uow) -> GetUserNestedProgressDTO:
        user_tasks = user.tasks
        user_progress = user.progress
        user_tasks_exercises_ids = set()
        user_progress_exercises_ids = [progress.exercise_id for progress in user_progress]

        for task in user_tasks:
            match task.task_type:
                case TaskTypes.EXERCISE:
                    user_tasks_exercises_ids.add(task.task_id)
                case TaskTypes.LESSON:
                    lesson = await uow.lesson_repository.get_by_id(task.task_id)
                    if not lesson:
                        continue

                    user_tasks_exercises_ids.update([exercise.exercise_id for exercise in lesson.exercises])
                case TaskTypes.COURSE:
                    course = await uow.course_repository.get_by_id(task.task_id)
                    if not course:
                        continue

                    for lesson in course.lessons:
                        user_tasks_exercises_ids.update([exercise.exercise_id for exercise in lesson.exercises])
                    for exercise in course.exercises:
                        user_tasks_exercises_ids.add(exercise.exercise_id)

        for task_exercise_id in user_tasks_exercises_ids:
            if task_exercise_id in user_progress_exercises_ids:
                continue

            user_progress = UsersProgress(
                user_id=user.user_id,
                exercise_id=task_exercise_id
            )
            user.progress.append(user_progress)

        await uow.flush()

        user = await sqlalchemy_to_pydantic(
            user,
            GetUserNestedProgressDTO
        )

        return user

    async def update_progress_by_user_id(self, user_id: int) -> GetUserNestedProgressDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)  # TODO: User must be as DTO object

            user = await self._update_students_progress(user, uow)
            return user

    async def update_progress(self) -> list[GetUserNestedProgressDTO]:
        async with self.uow as uow:
            updated_users = []
            users = await uow.user_repository.get_all_students()

            for user in users:
                # TODO: Add validation is student
                _user = await self._update_students_progress(user, uow)
                updated_users.append(_user)

            return updated_users
