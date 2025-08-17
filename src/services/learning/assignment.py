from typing import Callable, TypeVar, Awaitable, Sequence

from src.uow.abstract import AbstractUoW
from src.core.exceptions import ExerciseNotFound, UserNotFound, LessonsNotFound, CoursesNotFound
from src.core.orm_to_dto import many_sqlalchemy_to_pydantic, sqlalchemy_to_pydantic
from src.dto.users.assignments import GetUserNestedTasksDTO, GetUserNestedProgressDTO, GetUserNestedDTO, FilterUserDTO
from src.dto.learning.assignment import UpdateAssignedTasksDTO
from src.schemas.enums import TaskTypes, UsersRoles
from src.models.users_tasks import UsersTasks
from src.models.m2m import UsersProgress
from src.models.users import Users
from src.validators.users import validate_user_is_student
from src.validators.common import is_update_relation_ids_is_valid, validate_all_ids_found
from src.services.student.helper import StudentHelper


T = TypeVar("T")


class AssignmentService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow
        self.student_helper = StudentHelper()

    async def get_all_students(self) -> list[GetUserNestedDTO]:
        async with self.uow as uow:
            filter = FilterUserDTO(
                role=UsersRoles.USER
            )
            users = await uow.user_repository.get_all_full_nested(filter)
            users = await many_sqlalchemy_to_pydantic(
                users,
                GetUserNestedDTO
            )

            return users

    async def _update_user_tasks(
            self,
            entity: T,
            add_ids: list[int],
            delete_ids: list[int],
            task_type: TaskTypes,
            get_entities_by_ids: Callable[[list[int]], Awaitable[Sequence[T]]],
            entity_id_getter: Callable[[T], int],
            exception: type[Exception],
            uow
    ) -> None:

        entities = await get_entities_by_ids(add_ids + delete_ids)
        validate_all_ids_found(
            input_ids=add_ids + delete_ids,
            founded_objects=entities,
            id_getter_function=entity_id_getter,
            exception_builder=exception
        )

        assigned_tasks = await uow.users_tasks_repository.get_by_task_type(entity.user_id, task_type)
        assigned_ids = [t.task_id for t in assigned_tasks] if assigned_tasks else []
        is_update_relation_ids_is_valid(
            relation_ids=assigned_ids,
            add_relation_ids=add_ids,
            delete_relation_ids=delete_ids,
        )

        for entity_id in add_ids:
            if entity_id not in assigned_ids:
                entity.tasks.append(UsersTasks(task_id=entity_id, task_type=task_type))

        for assigned_task in assigned_tasks:
            if assigned_task.task_id in delete_ids:
                entity.tasks.remove(assigned_task)

        await uow.flush()

    async def update_exercises(self, user_id: int, data: UpdateAssignedTasksDTO) -> GetUserNestedTasksDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id_tasks_nested(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)

            await self._update_user_tasks(
                entity=user,
                add_ids=data.add_ids,
                delete_ids=data.delete_ids,
                task_type=TaskTypes.EXERCISE,
                get_entities_by_ids=uow.exercise_repository.get_by_ids,
                entity_id_getter=lambda e: e.exercise_id,
                exception=ExerciseNotFound,
                uow=uow
            )

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserNestedTasksDTO
            )

            return user

    async def update_lessons(self, user_id: int, data: UpdateAssignedTasksDTO) -> GetUserNestedTasksDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id_tasks_nested(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)

            await self._update_user_tasks(
                entity=user,
                add_ids=data.add_ids,
                delete_ids=data.delete_ids,
                task_type=TaskTypes.LESSON,
                get_entities_by_ids=uow.lesson_repository.get_by_ids,
                entity_id_getter=lambda l: l.lesson_id,
                exception=LessonsNotFound,
                uow=uow
            )

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserNestedTasksDTO
            )

            return user

    async def update_courses(self, user_id: int, data: UpdateAssignedTasksDTO) -> GetUserNestedTasksDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id_tasks_nested(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)

            await self._update_user_tasks(
                entity=user,
                add_ids=data.add_ids,
                delete_ids=data.delete_ids,
                task_type=TaskTypes.COURSE,
                get_entities_by_ids=uow.course_repository.get_by_ids,
                entity_id_getter=lambda c: c.course_id,
                exception=CoursesNotFound,
                uow=uow
            )

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserNestedTasksDTO
            )

            return user

    async def _update_students_progress(self, user: Users, uow) -> GetUserNestedProgressDTO:
        user_progress = user.progress

        user_tasks_exercises_ids = await self.student_helper.extract_exercise_ids_from_tasks(user, uow)
        user_progress_exercises_ids = [progress.exercise_id for progress in user_progress]

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
            user = await uow.user_repository.get_by_id_full_nested(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)

            user = await self._update_students_progress(user, uow)
            return user

    async def update_progress(self) -> list[GetUserNestedProgressDTO]:
        async with self.uow as uow:
            updated_users = []
            filter = FilterUserDTO(
                role=UsersRoles.USER
            )
            users = await uow.user_repository.get_all_full_nested(filter)

            for user in users:
                if user.role != UsersRoles.USER:
                    continue

                _user = await self._update_students_progress(user, uow)
                updated_users.append(_user)

            return updated_users
