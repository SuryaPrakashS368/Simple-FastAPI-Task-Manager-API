from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import SessionLocal
from app import schemas
from app.dependencies import allow_roles
from app.oauth2 import get_current_user
from app.Crud.activity import create_activity_log
from app.Crud.notification import create_notification
from app.Crud.auditLog import create_audit_log
from app.Crud import Task

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
    new_task = Task.create_task(db, task,current_user)

    create_activity_log(
    db=db,
    user_id=current_user.id,
    action="TASK_CREATED",
    entity_type="Task",
    entity_id=new_task.id,
    description=f"Task '{task.title}' created."
    )

    if task.assigned_to:

        create_notification(
        db=db,
        user_id=task.assigned_to,
        title="Task Assigned",
        message=f"You have been assigned '{task.title}'."
        )

        create_activity_log(
        db=db,
        user_id=current_user.id,
        action="TASK_ASSIGNED",
        entity_type="Task",
        entity_id=new_task.id,
        description=f"Task '{task.title}' assigned."
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

    return Task.get_tasks(
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

    task = Task.get_task(db, task_id)

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

    db_task = Task.get_task(db, task_id)

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

    old_task = Task.get_task(db, task_id)
    old_priority = old_task.priority
    old_status = db_task.status
    old_due_date = db_task.due_date
    old_assigned_to = db_task.assigned_to

    updated_task = Task.update_task(db, task_id, task)

    if old_priority != updated_task.priority:

        create_audit_log(
        db=db,
        entity_type="Task",
        entity_id=updated_task.id,
        field_name="priority",
        old_value=old_priority,
        new_value=updated_task.priority,
        changed_by=current_user.id
        )

    if old_status != updated_task.status:

        create_activity_log(
        db=db,
        user_id=current_user.id,
        action="TASK_STATUS_CHANGED",
        entity_type="Task",
        entity_id=updated_task.id,
        description=f"Status changed from {old_status} to {updated_task.status}"
        )

        create_audit_log(
        db=db,
        entity_type="Task",
        entity_id=updated_task.id,
        field_name="status",
        old_value=old_status,
        new_value=updated_task.status,
        changed_by=current_user.id
        )

        create_notification(
        db=db,
        user_id=updated_task.assigned_to,
        title="Task Status Updated",
        message=f"Task '{updated_task.title}' is now {updated_task.status}."
        )

    if old_due_date != updated_task.due_date:

        create_activity_log(
        db=db,
        user_id=current_user.id,
        action="TASK_DEADLINE_UPDATED",
        entity_type="Task",
        entity_id=updated_task.id,
        description="Task deadline updated."
        )

        create_audit_log(
        db=db,
        entity_type="Task",
        entity_id=updated_task.id,
        field_name="due_date",
        old_value=str(old_due_date),
        new_value=str(updated_task.due_date),
        changed_by=current_user.id
        )   

    if old_assigned_to != updated_task.assigned_to:

        create_activity_log(
        db=db,
        user_id=current_user.id,
        action="TASK_REASSIGNED",
        entity_type="Task",
        entity_id=updated_task.id,
        description=f"Task '{updated_task.title}' reassigned."
        )

        create_notification(
        db=db,
        user_id=updated_task.assigned_to,
        title="Task Reassigned",
        message=f"You have been assigned '{updated_task.title}'."
        )

    return updated_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(allow_roles(["Admin", "Manager"]))
):

    task = Task.delete_task(db, task_id)
    
    create_activity_log(
    db=db,
    user_id=current_user.id,
    action="DELETE_TASK",
    entity_type="Task",
    entity_id=task.id,
    description=f"Deleted task '{task.title}'"
    )
    if task is None:
        raise HTTPException(404, "Task not found")

    return {
        "message": "Task deleted successfully"
    }