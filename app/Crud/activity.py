from sqlalchemy.orm import Session
from app.models import ActivityLog
from .. import models
from .. import schemas

def create_activity_log(
    db: Session,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    description: str
):

    activity = models.ActivityLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def get_user_activities(
    db: Session,
    user_id: int
):

    return (
        db.query(models.ActivityLog)
        .filter(models.ActivityLog.user_id == user_id)
        .order_by(models.ActivityLog.created_at.desc())
        .all()
    )

def get_all_activities(db: Session):

    return (
        db.query(models.ActivityLog)
        .order_by(models.ActivityLog.created_at.desc())
        .all()
    )

def get_project_activities(
    db: Session,
    project_id: int
):

    return (
        db.query(models.ActivityLog)
        .filter(
            models.ActivityLog.entity_type == "Project",
            models.ActivityLog.entity_id == project_id
        )
        .order_by(models.ActivityLog.created_at.desc())
        .all()
    )

def filter_activity_by_action(
    db: Session,
    action: str
):

    return (
        db.query(models.ActivityLog)
        .filter(models.ActivityLog.action == action)
        .all()
    )

from datetime import datetime

def filter_activity_by_date(
    db: Session,
    start_date: datetime,
    end_date: datetime
):

    return (
        db.query(models.ActivityLog)
        .filter(
            models.ActivityLog.created_at >= start_date,
            models.ActivityLog.created_at <= end_date
        )
        .all()
    )
