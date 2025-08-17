from src.schemas.users.base import UserSchemaBase


class UserNestedTasksSchema(UserSchemaBase):
    tasks: list["AssignmentSchema"]


class UserNestedProgressSchema(UserSchemaBase):
    progress: list["UsersProgressSchema"]


class UserNestedSchema(UserNestedTasksSchema, UserNestedProgressSchema):
    pass
