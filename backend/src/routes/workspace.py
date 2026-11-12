from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db
from src.middlewares.auth import get_current_user
from src.models.workspace import Workspace
from src.schemas.workspace import WorkspaceRead

router = APIRouter(prefix="/workspace", tags=["workspace"])


@router.get("", response_model=WorkspaceRead)
def detail(db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = db.scalar(select(Workspace))
    if not item:
        raise HTTPException(status_code=404, detail="工作区尚未初始化")
    return WorkspaceRead.model_validate(item)
