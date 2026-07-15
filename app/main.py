from fastapi import FastAPI

from .database import Base
from .database import engine

from . import models

from .routes.user import router as user_router
from .routes.task import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="FastAPI Task Manager with JWT Authentication",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(task_router)


@app.get("/")
def home():
    return {
        "message": "Task Manager API Running Successfully"
    }