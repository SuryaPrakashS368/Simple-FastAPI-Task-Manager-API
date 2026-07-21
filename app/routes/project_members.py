from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.dependencies import allow_roles
from app.oauth2 import get_current_user
from app import schemas
from app import crud
router = APIRouter(
    prefix="/projects",
    tags=["Project Members"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/{project_id}/members",
    response_model=schemas.ProjectMemberResponse
)

def add_project_member(
    project_id: int,
    request: schemas.AddMember,
    db: Session = Depends(get_db),
    current_user=Depends(
        allow_roles(
            ["Admin", "Manager"]
        )
    )
):

    member = crud.add_member(
        db,
        project_id,
        request.user_id
    )

    if member is None:
        raise HTTPException(
            status_code=400,
            detail="User already exists in project"
        )

    return member


@router.get(
    "/{project_id}/members",
    response_model=list[schemas.ProjectMemberResponse]
)

def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return crud.get_members(
        db,
        project_id
    )


@router.delete(
    "/{project_id}/members/{user_id}"
)

def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        allow_roles(
            ["Admin", "Manager"]
        )
    )
):

    member = crud.remove_member(
        db,
        project_id,
        user_id
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return {
        "message": "Member removed successfully"
    }