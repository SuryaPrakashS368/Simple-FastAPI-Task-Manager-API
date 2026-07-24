from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.Crud import notification
from app.dependencies import get_current_user
from app import models

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return notification.get_notifications(
        db=db,
        user_id=current_user.id
    )

@router.get("/unread")
def unread_notifications(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return notification.get_unread_notifications(
        db=db,
        user_id=current_user.id
    )

@router.put("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return notification.mark_notification_read(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )

@router.put("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return notification.mark_all_notifications_read(
        db=db,
        user_id=current_user.id
    )

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return notification.delete_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )        