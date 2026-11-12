from sqlalchemy.orm import Session

from src.schemas.audit_log import AuditList, AuditRead
from src.services import audit_service


def list_items(db: Session) -> AuditList:
    items = audit_service.list_recent(db)
    return AuditList(items=[AuditRead.model_validate(item) for item in items], total=len(items))
