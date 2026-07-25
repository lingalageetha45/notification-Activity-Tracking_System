from sqlalchemy.orm import Session

from ..models import AuditLog


def log_audit(
    db: Session,
    entity_type: str,
    entity_id: int,
    field_name: str,
    old_value: str,
    new_value: str,
    changed_by: int
):
    audit = AuditLog(
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