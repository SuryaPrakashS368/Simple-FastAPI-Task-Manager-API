from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.dependencies import allow_roles
from app.oauth2 import get_current_user
from app import schemas
from app.Crud import projectMember
from app.Crud.activity import create_activity_log
from app.Crud.notification import create_notification
from app.Crud.auditLog import create_audit_log

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

    member = projectMember.add_member(
        db,
        project_id,
        request.user_id
    )

    if member is None:
        raise HTTPException(
            status_code=400,
            detail="User already exists in project"
        )

    create_activity_log(
    db=db,
    user_id=current_user.id,
    action="MEMBER_ADDED",
    entity_type="Project",
    entity_id=project_id,
    description="Member added to project."
    )

    create_notification(
    db=db,
    user_id=current_user.id,
    title="Project Invitation",
    message="You have been added to the project."
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

    return projectMember.get_members(
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

    member = projectMember.remove_member(
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