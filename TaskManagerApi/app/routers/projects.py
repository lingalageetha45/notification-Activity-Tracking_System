from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .. import crud, schemas
from ..dependencies import get_current_user
from ..models import User
from ..utils.permissions import require_admin_or_manager

router = APIRouter(
    prefix="/projects",
    tags=["Project Members"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{project_id}/members")
def add_project_member(
    project_id: int,
    member: schemas.ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin_or_manager(current_user)

    return crud.add_project_member(
        db=db,
        project_id=project_id,
        user_id=member.user_id,
        current_user=current_user
    )


@router.get("/{project_id}/members")
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_project_members(
        db=db,
        project_id=project_id
    )


@router.delete("/{project_id}/members/{user_id}")
def remove_project_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin_or_manager(current_user)

    member = crud.remove_project_member(
        db=db,
        project_id=project_id,
        user_id=user_id,
        current_user=current_user
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return {
        "message": "Member removed successfully"
    }