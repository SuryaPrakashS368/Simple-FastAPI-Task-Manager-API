from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    Pending = "Pending"
    Completed = "Completed"

# -------------------------
# User Schemas
# -------------------------

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# Task Schemas
# -------------------------

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.Pending


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: str
    user_id: int

    class Config:
        from_attributes = True


# -------------------------
# Login Schemas
# -------------------------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None        

class TaskPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
