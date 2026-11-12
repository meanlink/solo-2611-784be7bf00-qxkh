from src.schemas.common import ORMModel, Timestamped


class AuditRead(Timestamped):
    id: str
    action: str
    resource_type: str
    resource_id: str
    actor_id: str
    detail: dict


class AuditList(ORMModel):
    items: list[AuditRead]
    total: int
