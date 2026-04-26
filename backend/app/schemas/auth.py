from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Auth schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class TokenResponse(BaseModel):
    token: str
    token_type: str = "Bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    real_name: str
    phone: str
    email: str
    roles: list[str] = []
    status: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


# User schemas
class UserCreate(BaseModel):
    username: str
    real_name: str = ""
    password: str
    phone: str = ""
    email: str = ""
    role_ids: list[int] = []


class UserUpdate(BaseModel):
    real_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    role_ids: Optional[list[int]] = None
    status: Optional[int] = None


# Role schemas
class RoleResponse(BaseModel):
    id: int
    role_name: str
    role_desc: str
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True
