from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from src.schemas.enums import UsersRoles
from src.dto.base import TimestampedDTO


class GetUserDTOBase(TimestampedDTO):
    user_id: int
    login: str
    password_hash: str
    email: Optional[EmailStr] = None
    role: UsersRoles


class CreateUserDTOBase(BaseModel):
    login: str
    password_hash: str
    email: Optional[EmailStr] = None
    role: UsersRoles


class UpdateUserDTOBase(BaseModel):
    login: Optional[str] = None
    password_hash: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UsersRoles] = None

