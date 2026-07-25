from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum


# ======================================================
# ENUMS
# ======================================================

class UserRole(str, Enum):
    Admin = "Admin"
    Manager = "Manager"
    Member = "Member"


class TaskStatus(str, Enum):
    Pending = "Pending"
    InProgress = "In Progress"
    Completed = "Completed"


class TaskPriority(str, Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"


# ======================================================
# USER SCHEMAS
# ======================================================

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.Member


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


# ======================================================
# PROJECT SCHEMAS
# ======================================================

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_by: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ======================================================
# PROJECT MEMBER SCHEMAS
# ======================================================

class ProjectMemberCreate(BaseModel):
    user_id: int


class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# ======================================================
# TASK SCHEMAS
# ======================================================

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.Medium
    due_date: Optional[datetime] = None
    project_id: int
    assigned_to: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    project_id: int
    assigned_to: int

    model_config = ConfigDict(from_attributes=True)


# ======================================================
# NOTIFICATION SCHEMAS
# ======================================================

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ======================================================
# ACTIVITY LOG SCHEMAS
# ======================================================

class ActivityLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    entity_type: str
    entity_id: int
    description: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ======================================================
# AUDIT LOG SCHEMAS
# ======================================================

class AuditLogResponse(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    field_name: str
    old_value: Optional[str]
    new_value: Optional[str]
    changed_by: int
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)