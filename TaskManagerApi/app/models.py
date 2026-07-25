from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


# ==========================
# User
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="Member")
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship(
        "Task",
        back_populates="assignee",
        cascade="all, delete"
    )

    created_projects = relationship(
        "Project",
        back_populates="creator",
        cascade="all, delete"
    )

    memberships = relationship(
        "ProjectMember",
        back_populates="user",
        cascade="all, delete"
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete"
    )

    activities = relationship(
        "ActivityLog",
        back_populates="user",
        cascade="all, delete"
    )

    audit_logs = relationship(
        "AuditLog",
        back_populates="changed_by_user",
        cascade="all, delete"
    )


# ==========================
# Project
# ==========================
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship(
        "User",
        back_populates="created_projects"
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


# ==========================
# Project Member
# ==========================
class ProjectMember(Base):
    __tablename__ = "project_members"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "user_id",
            name="uq_project_user"
        ),
    )

    id = Column(Integer, primary_key=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    project = relationship(
        "Project",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="memberships"
    )


# ==========================
# Task
# ==========================
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)

    description = Column(String(500))

    status = Column(String(20), default="Pending")

    priority = Column(String(20), default="Medium")

    due_date = Column(DateTime)

    assigned_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id")
    )

    assignee = relationship(
        "User",
        back_populates="tasks"
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )


# ==========================
# Notification
# ==========================
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String(200), nullable=False)

    message = Column(Text, nullable=False)

    is_read = Column(Boolean, default=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="notifications"
    )


# ==========================
# Activity Log
# ==========================
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    action = Column(String(100), nullable=False)

    entity_type = Column(String(50), nullable=False)

    entity_id = Column(Integer, nullable=False)

    description = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="activities"
    )


# ==========================
# Audit Log
# ==========================
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    entity_type = Column(String(50), nullable=False)

    entity_id = Column(Integer, nullable=False)

    field_name = Column(String(100), nullable=False)

    old_value = Column(Text)

    new_value = Column(Text)

    changed_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    changed_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    changed_by_user = relationship(
        "User",
        back_populates="audit_logs"
    )