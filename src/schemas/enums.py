from enum import Enum


class UsersRoles(Enum):
    ADMIN = "admin"
    USER = "user"


class ExerciseTypes(Enum):
    SCHULTE = "schulte"
    DARKENED = "darkened"
    EFFECTIVE = "effective"
    BLOCKS = "blocks"
    TABLES = "tables"
