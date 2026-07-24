from sqlalchemy.orm import Session
from app.models import ActivityLog
from .. import models
from .. import schemas

def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str
):
    notification = models.Notification(
        user_id=user_id,
        title=title,
        message=message
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification

def get_notifications(db: Session, user_id: int):

    return (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id)
        .order_by(models.Notification.created_at.desc())
        .all()
    )

def get_unread_notifications(db: Session, user_id: int):

    return (
        db.query(models.Notification)
        .filter(
            models.Notification.user_id == user_id,
            models.Notification.is_read == False
        )
        .all()
    )   

def mark_notification_read(
    db: Session,
    notification_id: int,
    user_id: int
):

    notification = (
        db.query(models.Notification)
        .filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == user_id
        )
        .first()
    )

    if notification:
        notification.is_read = True
        db.commit()
        db.refresh(notification)

    return notification

def mark_all_notifications_read(
    db: Session,
    user_id: int
):

    notifications = (
        db.query(models.Notification)
        .filter(
            models.Notification.user_id == user_id,
            models.Notification.is_read == False
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
    user_id: int
):

    notification = (
        db.query(models.Notification)
        .filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == user_id
        )
        .first()
    )

    if notification:
        db.delete(notification)
        db.commit()

    return notification