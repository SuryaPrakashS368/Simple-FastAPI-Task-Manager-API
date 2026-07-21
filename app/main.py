from fastapi import FastAPI

from app.middleware import RequestLoggingMiddleware
from .database import Base
from .database import engine
from . import models
from .routes.user import router as user_router
from .routes.task import router as task_router
from .routes.projects import router as projects_router
from .routes.project_members import router as project_members_router
from .routes.analytics import router as analytics_router
from app.exceptions import global_exception_handler

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="FastAPI Task Manager with JWT Authentication",
    version="1.0.0"
)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(user_router)
app.include_router(task_router)
app.include_router(projects_router)
app.include_router(project_members_router)
app.include_router(analytics_router)
app.add_exception_handler(
    Exception,
    global_exception_handler
)

@app.get("/")
def home():
    return {
        "message": "Task Manager API Running Successfully"
    }