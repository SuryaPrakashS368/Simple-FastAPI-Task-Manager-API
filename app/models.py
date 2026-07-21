from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

from datetime import datetime

# -------------------------
# User
# -------------------------

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="Member")
    created_at = Column(DateTime, default=datetime.utcnow)
    projects = relationship(
        "Project",
        back_populates="creator"
    )
    assigned_tasks = relationship(
        "Task",
        back_populates="assignee"
    )
    project_members = relationship(
    "ProjectMember",
    back_populates="user",
    cascade="all, delete"
)

# -------------------------
# Project
# -------------------------

class Project(Base):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    is_deleted = Column(Boolean, default=False)
    creator = relationship(
        "User",
        back_populates="projects"
    )
    members = relationship(
    "ProjectMember",
    back_populates="project",
    cascade="all, delete"
    )
    tasks = relationship(
    "Task",
    back_populates="project",
    cascade="all, delete"
    )


class ProjectMember(Base):

    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )
    project = relationship(
        "Project",
        back_populates="members"
    )
    user = relationship(
        "User",
        back_populates="project_members"
    )    

# -------------------------
# Task
# -------------------------

class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="Pending")
    priority = Column(String, default="Medium")
    due_date = Column(DateTime)
    assigned_to = Column(
        Integer,
        ForeignKey("users.id")
    )
    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )
    assignee = relationship(
        "User",
        back_populates="assigned_tasks"
    )
    project = relationship(
    "Project",
    back_populates="tasks"
)
    is_deleted = Column(Boolean, default=False)


# -------------------------
# Analytics
# -------------------------
class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    description = Column(Text)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )