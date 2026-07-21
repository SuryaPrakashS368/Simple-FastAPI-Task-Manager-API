from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    Pending = "Pending"
    InProgress = "In Progress"
    Completed = "Completed"

class Priority(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"

# -------------------------
# User Schemas
# -------------------------

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "Member"

class UserLogin(BaseModel):
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
# Project Schemas
# -------------------------
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str]

# -------------------------
# Task Schemas
# -------------------------

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status:TaskStatus
    priority:Priority
    due_date: datetime
    assigned_to: int
    project_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: datetime
    assigned_to: int
    project_id: int

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

# -------------------------
# Project
# ------------------------

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_by: int
    created_at: datetime
    class Config:
        from_attributes = True


class AddMember(BaseModel):

    user_id: int        


class ProjectMemberResponse(BaseModel):

    id: int
    project_id: int
    user_id: int

    class Config:
        from_attributes = True