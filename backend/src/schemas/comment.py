from src.schemas.common import ORMModel, Timestamped


class CommentRead(Timestamped):
    id: str
    body: str
    decision: str
    run_id: str
    author_id: str
