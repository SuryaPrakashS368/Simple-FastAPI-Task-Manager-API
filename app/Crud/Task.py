from sqlalchemy.orm import Session
from app.models import ActivityLog
from .. import models
from .. import schemas
from .notification import create_notification

def create_task(db: Session, task: schemas.TaskCreate,user_id: int):

    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
        project_id=task.project_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    create_notification(
    db=db,
    user_id=db_task.assigned_to,
    title="Task Assigned",
    message=f"You have been assigned task '{db_task.title}'."
)

    return db_task

def get_tasks(
    db: Session,
    status: str = None,
    priority: str = None,
    assigned_to: int = None
):

    query = db.query(models.Task).filter(
    models.Task.is_deleted == False
)

    if status:
        query = query.filter(
            models.Task.status == status
        )

    if priority:
        query = query.filter(
            models.Task.priority == priority
        )

    if assigned_to:
        query = query.filter(
            models.Task.assigned_to == assigned_to
        )

    return query.all()


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()


def update_task(
    db: Session,
    task_id: int,
    task: schemas.TaskUpdate
):

    db_task = get_task(db, task_id)
    if db_task is None:
        return None

    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task is None:
        return None

    db_task.is_deleted = True
    db.commit()

    return db_task
