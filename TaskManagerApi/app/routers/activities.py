from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..dependencies import get_current_user
from ..models import User
from .. import crud

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_all_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_activities(db)


@router.get("/user/{user_id}")
def get_user_activities(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_user_activities(
        db,
        user_id
    )


@router.get("/project/{project_id}")
def get_project_activities(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_project_activities(
        db,
        project_id
    )


@router.get("/action/{action}")
def filter_by_action(
    action: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.filter_activities_by_action(
        db,
        action
    )


@router.get("/date")
def filter_by_date(
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.filter_activities_by_date(
        db,
        start_date,
        end_date
    )