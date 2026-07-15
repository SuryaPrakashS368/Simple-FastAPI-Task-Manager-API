from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from typing import Optional
from fastapi import Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from ..database import get_db

from ..oauth2 import get_current_user

from .. import crud
from .. import schemas
from .. import models

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "/",
    response_model=schemas.TaskResponse
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return crud.create_task(
        db,
        task,
        current_user.id
    )

@router.get(
    "/",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(
    status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    query = db.query(models.Task).filter(
        models.Task.user_id == current_user.id
    )

    if status:
        query = query.filter(models.Task.status == status)

    tasks = query.offset(skip).limit(limit).all()

    return tasks

@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    task = crud.get_task(
        db,
        task_id,
        current_user.id
    )

    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    return task


@router.put(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    updated_task = crud.update_task(
        db,
        task_id,
        task,
        current_user.id
    )

    if updated_task is None:

        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    return updated_task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    deleted_task = crud.delete_task(
        db,
        task_id,
        current_user.id
    )

    if deleted_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task Not Found"
        )

    return JSONResponse(
        status_code=200,
        content={
            "message": "Task Deleted Successfully"
        }
    )

@router.patch(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def patch_task(
    task_id: int,
    task: schemas.TaskPatch,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    updated_task = crud.patch_task(
        db,
        task_id,
        task,
        current_user.id
    )

    if updated_task is None:
        raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task Not Found"
)

    return updated_task