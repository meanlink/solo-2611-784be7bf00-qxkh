import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.dataset import Dataset
from src.models.workspace import Workspace


def list_datasets(db: Session) -> list[Dataset]:
    return list(db.scalars(select(Dataset).order_by(Dataset.created_at.desc())))


def get_dataset(db: Session, dataset_id: str) -> Dataset | None:
    return db.get(Dataset, dataset_id)


def create_dataset(db: Session, workspace: Workspace, user_id: str,
                   name: str, source: str, description: str, rows: list[dict]) -> Dataset:
    serialized = json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()
    natural_key = f"{workspace.id}:{name}:{hashlib.sha1(serialized).hexdigest()[:12]}"
    existing = db.scalar(select(Dataset).where(Dataset.natural_key == natural_key))
    if existing:
        return existing
    item = Dataset(
        natural_key=natural_key,
        name=name,
        source=source,
        description=description,
        rows=rows,
        row_count=len(rows),
        checksum=hashlib.sha256(serialized).hexdigest(),
        workspace_id=workspace.id,
        created_by=user_id,
        status="ready",
    )
    db.add(item)
    db.flush()
    return item
