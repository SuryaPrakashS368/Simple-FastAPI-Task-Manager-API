from sqlalchemy.orm import Session
from app.models import ActivityLog
from .. import models
from .. import schemas

def create_project(
    db: Session,
    project: schemas.ProjectCreate,
    user_id: int
):

    db_project = models.Project(
        name=project.name,
        description=project.description,
        created_by=user_id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str = ""
):

    query = db.query(models.Project).filter(
    models.Project.is_deleted == False
)

    if search:
        query = query.filter(
            models.Project.name.ilike(f"%{search}%")
        )
    return query.offset(skip).limit(limit).all()


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(
    models.Project.id == project_id,
    models.Project.is_deleted == False
).first()


def update_project(
    db: Session,
    project_id: int,
    project: schemas.ProjectCreate,
    user_id: int
):

    db_project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if db_project is None:
        return None

    db_project.name = project.name
    db_project.description = project.description

    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(
    db: Session,
    project_id: int,
    user_id: int
):

    project = db.query(models.Project).filter(
        models.Project.id == project_id
    ).first()

    if project is None:

        return None

    project.is_deleted = True
    db.commit()

    return project