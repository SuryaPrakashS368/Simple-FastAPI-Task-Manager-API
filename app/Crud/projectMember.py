from sqlalchemy.orm import Session
from app.models import ActivityLog
from .. import models
from .. import schemas

def add_member(
    db: Session,
    project_id: int,
    user_id: int
):

    member = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id,
        models.ProjectMember.user_id == user_id
    ).first()

    if member:
        return None

    new_member = models.ProjectMember(
        project_id=project_id,
        user_id=user_id
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


def get_members(
    db: Session,
    project_id: int
):

    return db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id
    ).all()


def remove_member(
    db: Session,
    project_id: int,
    user_id: int
):

    member = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id,
        models.ProjectMember.user_id == user_id
    ).first()

    if member is None:
        return None

    db.delete(member)
    db.commit()

    return member