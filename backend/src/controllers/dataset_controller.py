from sqlalchemy.orm import Session

from src.models.workspace import Workspace
from src.schemas.dataset import DatasetCreate, DatasetList, DatasetRead
from src.services import audit_service, dataset_service


def list_items(db: Session) -> DatasetList:
    items = dataset_service.list_datasets(db)
    return DatasetList(items=[DatasetRead.model_validate(item) for item in items], total=len(items))


def create_item(db: Session, payload: DatasetCreate, user, workspace: Workspace) -> DatasetRead:
    item = dataset_service.create_dataset(
        db, workspace, user.id, payload.name, payload.source, payload.description, payload.rows
    )
    audit_service.record(db, "dataset.create", "dataset", item.id, user.id, {"rows": item.row_count})
    db.commit()
    db.refresh(item)
    return DatasetRead.model_validate(item)
