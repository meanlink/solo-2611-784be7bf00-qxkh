from src.schemas.common import ORMModel, Timestamped


class WorkspaceRead(Timestamped):
    id: str
    name: str
    client_name: str
    context_note: str
    owner_id: str
