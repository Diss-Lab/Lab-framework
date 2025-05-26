from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.usage_log import UsageLog
from app.schemas.usage_log import UsageLogCreate, UsageLogRead
from app.database import get_db
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/logs", tags=["使用日志"])

@router.post("/", response_model=UsageLogRead, summary="添加使用日志")
def create_log(log_in: UsageLogCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    log = UsageLog(
        user_id=current_user.id,
        **log_in.dict()
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@router.get("/", response_model=List[UsageLogRead], summary="查询所有日志")
def list_logs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    logs = db.query(UsageLog).order_by(UsageLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs
