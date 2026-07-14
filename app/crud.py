from sqlalchemy.orm import Session
import models

def create_task(db: Session, task):

    new_task = models.Task(

        title=task.title,

        description=task.description,

        status=task.status

    )

    db.add(new_task)

    db.commit()

    db.refresh(new_task)

    return new_task


def get_tasks(db: Session):

    return db.query(models.Task).all()


def update_task(db: Session, task_id: int, task):

    db_task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if db_task is None:

        return None

    if task.title is not None:
        db_task.title = task.title

    if task.description is not None:
        db_task.description = task.description

    if task.status is not None:
        db_task.status = task.status


    db.commit()

    db.refresh(db_task)

    return db_task


def delete_task(db: Session, task_id: int):

    db_task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if db_task is None:

        return None

    db.delete(db_task)

    db.commit()

    return db_task