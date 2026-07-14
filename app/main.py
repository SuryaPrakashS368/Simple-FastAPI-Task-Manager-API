from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

import crud
import models

from database import engine
from database import SessionLocal

from schemas import TaskCreate
from schemas import TaskResponse
from schemas import TaskUpdate

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


@app.post("/tasks", response_model=TaskResponse)

def create(task: TaskCreate, db: Session = Depends(get_db)):

    return crud.create_task(db, task)


@app.get("/tasks", response_model=list[TaskResponse])

def read(db: Session = Depends(get_db)):

    return crud.get_tasks(db)


@app.put("/tasks/{task_id}")

def update(task_id: int, task: TaskUpdate,
           db: Session = Depends(get_db)):

    result = crud.update_task(db, task_id, task)

    if result is None:

        raise HTTPException(status_code=404,
                            detail="Task Not Found")

    return result


@app.delete("/tasks/{task_id}")

def delete(task_id: int,
           db: Session = Depends(get_db)):

    result = crud.delete_task(db, task_id)

    if result is None:

        raise HTTPException(status_code=404,
                            detail="Task Not Found")

    return {"message": "Task Deleted Successfully"}