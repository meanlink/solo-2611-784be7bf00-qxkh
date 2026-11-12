from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.controllers import analysis_controller
from src.database import get_db
from src.middlewares.auth import get_current_user, require_roles
from src.models.workspace import Workspace
from src.schemas.analysis import AnalysisCreate, AnalysisList, AnalysisRead

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.get("", response_model=AnalysisList)
def index(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return analysis_controller.list_items(db)


@router.post("", response_model=AnalysisRead)
def create(payload: AnalysisCreate, db: Session = Depends(get_db),
           user=Depends(require_roles("admin", "analyst"))):
    workspace = db.scalar(select(Workspace))
    if not workspace:
        raise HTTPException(status_code=409, detail="工作区尚未初始化")
    return analysis_controller.create_item(db, payload, user, workspace)


@router.get("/{analysis_id}", response_model=AnalysisRead)
def detail(analysis_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    from src.services.analysis_service import get_analysis
    item = get_analysis(db, analysis_id)
    if not item:
        raise HTTPException(status_code=404, detail="分析方案不存在")
    return AnalysisRead.model_validate(item)
