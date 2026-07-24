from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.Crud import auditLog
from app.dependencies import get_current_user
from app import models

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@router.get("/")
def get_all_audit_logs(

    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)

):

    return auditLog.get_audit_logs(db)

@router.get("/{entity_type}/{entity_id}")
def get_entity_audit_logs(

    entity_type: str,
    entity_id: int,

    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)

):

    return auditLog.get_audit_logs_by_entity(

        db=db,
        entity_type=entity_type,
        entity_id=entity_id

    )        