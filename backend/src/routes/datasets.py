from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.controllers import dataset_controller
from src.database import get_db
from src.middlewares.auth import get_current_user, require_roles
from src.models.workspace import Workspace
from src.schemas.dataset import DatasetCreate, DatasetList, DatasetRead

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("", response_model=DatasetList)
def index(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return dataset_controller.list_items(db)


@router.post("", response_model=DatasetRead)
def create(payload: DatasetCreate, db: Session = Depends(get_db),
           user=Depends(require_roles("admin", "analyst"))):
    workspace = db.scalar(select(Workspace))
    if not workspace:
        raise HTTPException(status_code=409, detail="工作区尚未初始化")
    return dataset_controller.create_item(db, payload, user, workspace)


@router.get("/{dataset_id}")
def detail(dataset_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from src.services.dataset_service import get_dataset
    item = get_dataset(db, dataset_id)
    if not item:
        raise HTTPException(status_code=404, detail="数据资产不存在")
    return DatasetRead.model_validate(item)
