from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
from datetime import datetime

# -------------------------
# User Model
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
# Project Model
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

# -------------------------
# Project Member Model
# -------------------------

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
# Task Model
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
# Notification Model
# -------------------------

class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())    

# -------------------------
# Activity Log Model
# -------------------------    

class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# -------------------------
# Audit Log Model
# -------------------------

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String)
    entity_id = Column(Integer)
    field_name = Column(String)
    old_value = Column(String)
    new_value = Column(String)
    changed_by = Column(Integer, ForeignKey("users.id"))
    changed_at = Column(DateTime(timezone=True), server_default=func.now())