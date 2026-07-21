from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import SessionLocal
from app import schemas
from app.dependencies import allow_roles
from app.oauth2 import get_current_user
from app.crud import create_log
from app import crud

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(allow_roles(["Admin", "Manager"]))
):
    new_task = crud.create_task(db, task)

    create_log(
        db=db,
        user_id=current_user.id,
        action="CREATE_TASK",
        description=f"Created task '{new_task.title}'"
    )

    return new_task


@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_tasks(
        db,
        status,
        priority,
        assigned_to
    )


@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    task = crud.get_task(db, task_id)

    if task is None:
        raise HTTPException(404, "Task not found")

    return task


@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    db_task = crud.get_task(db, task_id)

    if db_task is None:
        raise HTTPException(404, "Task not found")
    if current_user.role == "Member":
        if db_task.assigned_to != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You cannot update this task."
            )

        task.assigned_to = None
        task.priority = None
        task.due_date = None
        task.title = None
        task.description = None
    
    updated_task = crud.update_task(db, task_id, task)

    create_log(
    db=db,
    user_id=current_user.id,
    action="UPDATE_TASK",
    description=f"Updated task '{updated_task.title}'"
    )

    return updated_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(allow_roles(["Admin", "Manager"]))
):

    task = crud.delete_task(db, task_id)
    create_log(
    db=db,
    user_id=current_user.id,
    action="DELETE_TASK",
    description=f"Deleted task '{task.title}'"
    )
    if task is None:
        raise HTTPException(404, "Task not found")

    return {
        "message": "Task deleted successfully"
    }