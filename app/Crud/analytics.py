from sqlalchemy.orm import Session
from app.models import ActivityLog
from .. import models
from .. import schemas

def project_summary(
    db: Session,
    project_id: int
):

    total = db.query(models.Task).filter(
        models.Task.project_id == project_id
    ).count()

    pending = db.query(models.Task).filter(
        models.Task.project_id == project_id,
        models.Task.status == "Pending"
    ).count()

    progress = db.query(models.Task).filter(
        models.Task.project_id == project_id,
        models.Task.status == "In Progress"
    ).count()

    completed = db.query(models.Task).filter(
        models.Task.project_id == project_id,
        models.Task.status == "Completed"
    ).count()

    return {

        "total_tasks": total,
        "pending_tasks": pending,
        "in_progress_tasks": progress,
        "completed_tasks": completed

    }
