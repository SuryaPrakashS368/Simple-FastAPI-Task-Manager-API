from sqlalchemy.orm import Session

from . import models
from . import schemas
from .utils import hash_password


# -------------------------
# Get User by Email
# -------------------------

def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


# -------------------------
# Create User
# -------------------------

def create_user(db: Session, user: schemas.UserCreate):

    hashed_pwd = hash_password(user.password)

    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pwd
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


# -------------------------
# Authenticate User
# -------------------------

def authenticate_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        return None

    from .utils import verify_password

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user

# -------------------------
# Create Task
# -------------------------

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):

    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=user_id
    )

    db.add(db_task)

    db.commit()

    db.refresh(db_task)

    return db_task

def get_tasks(db: Session, user_id: int):

    return db.query(models.Task).filter(
        models.Task.user_id == user_id
    ).all()

def get_task(db: Session, task_id: int, user_id: int):

    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()

def update_task(
    db: Session,
    task_id: int,
    task: schemas.TaskUpdate,
    user_id: int
):

    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
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

def delete_task(
    db: Session,
    task_id: int,
    user_id: int
):

    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()

    if db_task is None:
        return None

    db.delete(db_task)

    db.commit()

    return db_task

def patch_task(
    db: Session,
    task_id: int,
    task: schemas.TaskPatch,
    user_id: int
):

    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()

    if db_task is None:
        return None

    update_data = task.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task