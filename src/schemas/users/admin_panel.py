from pydantic import EmailStr, Field
from typing import Optional

from src.schemas.enums import UsersRoles
from src.schemas.users.base import UserSchemaBase
from src.schemas.users.base import PasswordValidatorBase


class UserSchema(UserSchemaBase):
    pass


class UpdateUserSchema(PasswordValidatorBase):
    login: Optional[str] = Field(None, min_length=3, max_length=64)
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class CreateUserSchema(PasswordValidatorBase):
    login: str = Field(min_length=3, max_length=64)
    password: str
    email: Optional[EmailStr] = None
    role: UsersRoles
