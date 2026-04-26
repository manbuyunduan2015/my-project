from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
