from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.audit_log import AuditLog


def record(db: Session, action: str, resource_type: str, resource_id: str,
           actor_id: str, detail: dict | None = None) -> AuditLog:
    entry = AuditLog(action=action, resource_type=resource_type,
                     resource_id=resource_id, actor_id=actor_id, detail=detail or {})
    db.add(entry)
    return entry


def list_recent(db: Session, limit: int = 100) -> list[AuditLog]:
    return list(db.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)))
