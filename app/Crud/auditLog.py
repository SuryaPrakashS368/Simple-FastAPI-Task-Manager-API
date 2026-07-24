from sqlalchemy.orm import Session
from app.models import ActivityLog
from .. import models
from .. import schemas

def create_audit_log(
    db: Session,
    entity_type: str,
    entity_id: int,
    field_name: str,
    old_value: str,
    new_value: str,
    changed_by: int
):

    audit = models.AuditLog(
        entity_type=entity_type,
        entity_id=entity_id,
        field_name=field_name,
        old_value=old_value,
        new_value=new_value,
        changed_by=changed_by
    )

    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit

def get_audit_logs(db: Session):

    return (
        db.query(models.AuditLog)
        .order_by(models.AuditLog.changed_at.desc())
        .all()
    )

def get_audit_logs_by_entity(
    db: Session,
    entity_type: str,
    entity_id: int
):

    return (
        db.query(models.AuditLog)
        .filter(
            models.AuditLog.entity_type == entity_type,
            models.AuditLog.entity_id == entity_id
        )
        .order_by(models.AuditLog.changed_at.desc())
        .all()
    )

