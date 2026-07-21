from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.dependencies import allow_roles

from app.crud import project_summary

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/projects/{project_id}")

def analytics(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        allow_roles(
            ["Admin", "Manager"]
        )
    )
):

    return project_summary(
        db,
        project_id
    )