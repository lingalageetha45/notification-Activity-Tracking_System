from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import (
    User,
    Project,
    ProjectMember,
    Task,
    Notification,
    ActivityLog,
    AuditLog
)

from .schemas import (
    ProjectCreate,
    ProjectUpdate,
    TaskCreate,
    TaskUpdate
)

from .utils.notifier import send_notification
from .utils.activity_logger import log_activity
from .utils.audit import log_audit


# ======================================================
# PROJECT CRUD
# ======================================================

def create_project(
    db: Session,
    project: ProjectCreate,
    current_user: User
):
    db_project = Project(
        name=project.name,
        description=project.description,
        created_by=current_user.id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    log_activity(
        db=db,
        user_id=current_user.id,
        action="PROJECT_CREATED",
        entity_type="Project",
        entity_id=db_project.id,
        description=f"Created project '{db_project.name}'"
    )
    
    log_audit(
       db=db,
       entity_type="Project",
       entity_id=db_project.id,
       field_name="name",
       old_value="",
       new_value=db_project.name,
       changed_by=current_user.id
    )

    return db_project


def get_projects(db: Session):
    return db.query(Project).all()


def get_project(
    db: Session,
    project_id: int
):
    return (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )


def update_project(
    db: Session,
    project_id: int,
    project: ProjectUpdate
):
    db_project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not db_project:
        return None

    # Store old values
    old_name = db_project.name
    old_description = db_project.description

    # Update fields
    if project.name is not None:
        db_project.name = project.name

    if project.description is not None:
        db_project.description = project.description

    db.commit()
    db.refresh(db_project)

    # Activity log
    log_activity(
        db=db,
        user_id=db_project.created_by,
        action="PROJECT_UPDATED",
        entity_type="Project",
        entity_id=db_project.id,
        description="Project updated"
    )

    # Audit project name
    if old_name != db_project.name:
        log_audit(
            db=db,
            entity_type="Project",
            entity_id=db_project.id,
            field_name="name",
            old_value=old_name,
            new_value=db_project.name,
            changed_by=db_project.created_by
        )

    # Audit description
    if old_description != db_project.description:
        log_audit(
            db=db,
            entity_type="Project",
            entity_id=db_project.id,
            field_name="description",
            old_value=str(old_description),
            new_value=str(db_project.description),
            changed_by=db_project.created_by
        )

    return db_project


def delete_project(
    db: Session,
    project_id: int
):
    db_project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not db_project:
        return None

    log_activity(
        db=db,
        user_id=db_project.created_by,
        action="PROJECT_DELETED",
        entity_type="Project",
        entity_id=db_project.id,
        description="Project deleted"
    )

    log_audit(
        db=db,
        entity_type="Project",
        entity_id=db_project.id,
        field_name="deleted",
        old_value="Exists",
        new_value="Deleted",
        changed_by=db_project.created_by
    )

    db.delete(db_project)
    db.commit()

    return db_project


# ======================================================
# TASK CRUD
# ======================================================

def create_task(
    db: Session,
    task: TaskCreate,
    current_user: User
):
    db_task = Task(
        title=task.title,
        description=task.description,
        status="Pending",
        priority=task.priority.value,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
        project_id=task.project_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Send notification
    send_notification(
        db=db,
        user_id=task.assigned_to,
        title="New Task Assigned",
        message=f"You have been assigned task '{task.title}'."
    )

    # Activity log
    log_activity(
        db=db,
        user_id=current_user.id,
        action="TASK_CREATED",
        entity_type="Task",
        entity_id=db_task.id,
        description=f"Created task '{task.title}'"
    )

    # Audit log
    log_audit(
       db=db,
       entity_type="Task",
       entity_id=db_task.id,
       field_name="created",
       old_value="",
       new_value=db_task.title,
       changed_by=current_user.id
    )

    return db_task


def get_tasks(
    db: Session,
    current_user: User
):
    return (
        db.query(Task)
        .filter(Task.assigned_to == current_user.id)
        .all()
    )


def get_task(
    db: Session,
    task_id: int,
    current_user: User
):
    return (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.assigned_to == current_user.id
        )
        .first()
    )


def update_task(
    db: Session,
    task_id: int,
    task: TaskUpdate,
    current_user: User
):
    db_task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not db_task:
        return None

    old_status = db_task.status
    old_assigned = db_task.assigned_to

    if task.title is not None:
        db_task.title = task.title

    if task.description is not None:
        db_task.description = task.description

    if task.status is not None:
        db_task.status = task.status.value

    if task.priority is not None:
        db_task.priority = task.priority.value

    if task.due_date is not None:
        db_task.due_date = task.due_date

    if task.assigned_to is not None:
        db_task.assigned_to = task.assigned_to

    db.commit()
    db.refresh(db_task)

    log_activity(
        db=db,
        user_id=current_user.id,
        action="TASK_UPDATED",
        entity_type="Task",
        entity_id=db_task.id,
        description=f"Updated task '{db_task.title}'"
    )

    if old_status != db_task.status:
        log_audit(
            db=db,
            entity_type="Task",
            entity_id=db_task.id,
            field_name="status",
            old_value=old_status,
            new_value=db_task.status,
            changed_by=current_user.id
        )

    if old_assigned != db_task.assigned_to:
        send_notification(
            db=db,
            user_id=db_task.assigned_to,
            title="Task Reassigned",
            message=f"You have been assigned task '{db_task.title}'."
        )

        log_audit(
           db=db,
           entity_type="Task",
           entity_id=db_task.id,
           field_name="assigned_to",
           old_value=str(old_assigned),
           new_value=str(db_task.assigned_to),
           changed_by=current_user.id
        )

    return db_task


def delete_task(
    db: Session,
    task_id: int,
    current_user: User
):
    db_task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not db_task:
        return None

    task_title = db_task.title
    deleted_task_id = db_task.id

    log_activity(
        db=db,
        user_id=current_user.id,
        action="TASK_DELETED",
        entity_type="Task",
        entity_id=deleted_task_id,
        description=f"Deleted task '{task_title}'"
    )

    log_audit(
        db=db,
        entity_type="Task",
        entity_id=deleted_task_id,
        field_name="deleted",
        old_value="Exists",
        new_value="Deleted",
        changed_by=current_user.id
    )

    db.delete(db_task)
    db.commit()

    return db_task


# ======================================================
# PROJECT MEMBERS
# ======================================================

def add_project_member(
    db: Session,
    project_id: int,
    user_id: int,
    current_user: User
):
    # Debug prints
    print("========== ADD PROJECT MEMBER ==========")
    print("Project ID:", project_id)
    print("User ID:", user_id)
    print("Current User:", current_user.id)

    # Check if project exists
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    # Check if user exists
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check if already a member
    existing = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        )
        .first()
    )

    if existing:
        print("Member already exists:", existing.user_id)
        return existing

    # Create member
    member = ProjectMember(
        project_id=project_id,
        user_id=user_id
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    print("Saved Member")
    print("ID:", member.id)
    print("Project ID:", member.project_id)
    print("User ID:", member.user_id)

    # Notification
    send_notification(
        db=db,
        user_id=user_id,
        title="Added to Project",
        message=f"You were added to Project ID {project_id}"
    )

    # Activity Log
    log_activity(
        db=db,
        user_id=current_user.id,
        action="MEMBER_ADDED",
        entity_type="Project",
        entity_id=project_id,
        description=f"Added user {user_id} to project"
    )

    # Audit Log
    log_audit(
        db=db,
        entity_type="ProjectMember",
        entity_id=member.id,
        field_name="member",
        old_value="",
        new_value=str(user_id),
        changed_by=current_user.id
    )

    return member

def get_project_members(
    db: Session,
    project_id: int
):
    return (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )


def remove_project_member(
    db: Session,
    project_id: int,
    user_id: int,
    current_user: User
):
    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        )
        .first()
    )

    if not member:
        return None

    log_activity(
        db=db,
        user_id=current_user.id,
        action="MEMBER_REMOVED",
        entity_type="Project",
        entity_id=project_id,
        description=f"Removed user {user_id} from project"
    )

    log_audit(
       db=db,
       entity_type="ProjectMember",
       entity_id=member.id,
       field_name="member",
       old_value=str(user_id),
       new_value="Removed",
       changed_by=current_user.id
    )

    db.delete(member)
    db.commit()

    return member


# ======================================================
# NOTIFICATIONS
# ======================================================

def get_notifications(
    db: Session,
    current_user: User
):
    return (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def get_unread_notifications(
    db: Session,
    current_user: User
):
    return (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
        .order_by(Notification.created_at.desc())
        .all()
    )


def mark_notification_read(
    db: Session,
    notification_id: int,
    current_user: User
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
        .first()
    )

    if not notification:
        return None

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification


def mark_all_notifications_read(
    db: Session,
    current_user: User
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
        .all()
    )

    for notification in notifications:
        notification.is_read = True

    db.commit()

    return notifications


def delete_notification(
    db: Session,
    notification_id: int,
    current_user: User
):
    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
        .first()
    )

    if not notification:
        return None

    db.delete(notification)
    db.commit()

    return notification


# ======================================================
# ACTIVITY LOGS
# ======================================================

def get_activities(db: Session):
    return (
        db.query(ActivityLog)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )


def get_user_activities(
    db: Session,
    user_id: int
):
    return (
        db.query(ActivityLog)
        .filter(ActivityLog.user_id == user_id)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )


def get_project_activities(
    db: Session,
    project_id: int
):
    return (
        db.query(ActivityLog)
        .filter(
            ActivityLog.entity_type == "Project",
            ActivityLog.entity_id == project_id
        )
        .order_by(ActivityLog.created_at.desc())
        .all()
    )


def filter_activities_by_action(
    db: Session,
    action: str
):
    return (
        db.query(ActivityLog)
        .filter(ActivityLog.action == action)
        .order_by(ActivityLog.created_at.desc())
        .all()
    )


def filter_activities_by_date(
    db: Session,
    start_date,
    end_date
):
    return (
        db.query(ActivityLog)
        .filter(
            ActivityLog.created_at >= start_date,
            ActivityLog.created_at <= end_date
        )
        .order_by(ActivityLog.created_at.desc())
        .all()
    )


# ======================================================
# AUDIT LOGS
# ======================================================

def get_audit_logs(db: Session):
    return (
        db.query(AuditLog)
        .order_by(AuditLog.changed_at.desc())
        .all()
    )


def get_entity_audit_logs(
    db: Session,
    entity_type: str,
    entity_id: int
):
    return (
        db.query(AuditLog)
        .filter(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id
        )
        .order_by(AuditLog.changed_at.desc())
        .all()
    )