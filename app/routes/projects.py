from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Query
from app.database import SessionLocal
from app import schemas
from app import crud
from app.crud import create_log
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

    new_project = crud.create_project(
        db,
        project,
        current_user.id
    )

    create_log(
        db=db,
        user_id=current_user.id,
        action="CREATE_PROJECT",
        description=f"Created project '{new_project.name}'"
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

    return crud.get_projects(
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

    project = crud.get_project(
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

    updated = crud.update_project(
        db,
        project_id,
        project
    )
    create_log(
    db=db,
    user_id=current_user.id,
    action="UPDATE_PROJECT",
    description=f"Updated project '{updated.name}'"
    )
    if updated is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return updated


@router.delete("/{project_id}")

def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        allow_roles(["Admin"])
    )

):

    deleted = crud.delete_project(
        db,
        project_id
    )
    create_log(
    db=db,
    user_id=current_user.id,
    action="DELETE_PROJECT",
    description=f"Deleted project '{deleted.name}'"
    )
    if deleted is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return {
        "message": "Project deleted successfully"
    }