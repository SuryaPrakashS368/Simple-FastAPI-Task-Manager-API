from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
from app.database import SessionLocal
from app import schemas
from app.Crud import Project
from app.Crud.activity import create_activity_log
from app.Crud.auditLog import create_audit_log
from app.dependencies import allow_roles

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=schemas.ProjectResponse
)

def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        allow_roles(["Admin", "Manager"])
    )
):

    new_project = Project.create_project(
        db,
        project,
        current_user.id
    )

    create_activity_log(
    db=db,
    user_id=current_user.id,
    action="PROJECT_CREATED",
    entity_type="Project",
    entity_id=new_project.id,
    description=f"Project '{project.name}' created."
    )

    return new_project


@router.get(
    "/",
    response_model=list[schemas.ProjectResponse]
)

def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str = "",
    db: Session = Depends(get_db),
    current_user=Depends(
        allow_roles(["Admin", "Manager", "Member"])
    )

):

    return Project.get_projects(
        db,
        skip,
        limit,
        search
    )


@router.get(
    "/{project_id}",
    response_model=schemas.ProjectResponse
)

def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        allow_roles(["Admin", "Manager", "Member"])
    )

):

    project = Project.get_project(
        db,
        project_id
    )

    if project is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@router.put(
    "/{project_id}",
    response_model=schemas.ProjectResponse
)

def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        allow_roles(["Admin", "Manager"])
    )

):
    old_project = Project.get_project(db, project_id)
    old_description = old_project.description

    updated = Project.update_project(
        db,
        project_id,
        project,
        current_user
    )
    if updated is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    if old_description != updated.description:

        create_audit_log(
        db=db,
        entity_type="Project",
        entity_id=updated.id,
        field_name="description",
        old_value=old_description,
        new_value=updated.description,
        changed_by=current_user.id
        )

    create_activity_log(
    db=db,
    user_id=current_user.id,
    action="PROJECT_UPDATED",
    entity_type="Project",
    entity_id=updated.id,
    description=f"Project '{project.name}' updated."
    )

    create_audit_log(
    db=db,
    entity_type="Project",
    entity_id=updated.id,
    field_name="description",
    old_value=project.description,
    new_value=updated.description,
    changed_by=current_user.id
)

    return updated


@router.delete("/{project_id}")

def delete_project(
    project_id: int,
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        allow_roles(["Admin"])
    )

):

    deleted = Project.delete_project(
        db,
        project_id,
        current_user.id
    )

    if deleted is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
        
    create_activity_log(
    db=db,
    user_id=current_user.id,
    action="PROJECT_DELETED",
    entity_type="Project",
    entity_id=deleted.id,
    description=f"Project '{project.name}' deleted."
    )

    return {
        "message": "Project deleted successfully"
    }