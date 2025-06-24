from pydantic import BaseModel, EmailStr
from typing import Optional

from src.schemas.enums import UsersRoles


class GetUsersDTO(BaseModel):
    user_id: int
    login: str
    password_hash: str
    email: Optional[EmailStr] = None
    role: UsersRoles


class UpdateUsersDTO(BaseModel):
    login: Optional[str] = None
    password_hash: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UsersRoles] = None


class CreateUsersDTO(BaseModel):
    login: str
    password_hash: str
    email: Optional[EmailStr] = None
    role: UsersRoles
