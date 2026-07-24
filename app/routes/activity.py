from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.Crud import activity
from app.dependencies import get_current_user
from app import models

router = APIRouter(
    prefix="/activities",
    tags=["Activity Logs"]
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
    current_user: models.User = Depends(get_current_user)
):

    return activity.get_all_activities(db)


@router.get("/user/{user_id}")
def get_user_activity(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return activity.get_user_activities(
        db=db,
        user_id=user_id
    )

@router.get("/project/{project_id}")
def get_project_activity(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return activity.get_project_activities(
        db=db,
        project_id=project_id
    )

@router.get("/action/{action}")
def activity_by_action(
    action: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return activity.filter_activity_by_action(
        db=db,
        action=action
    )


@router.get("/date")
def activity_by_date(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return activity.filter_activity_by_date(
        db=db,
        start_date=start_date,
        end_date=end_date
    )