"""
使用日志相关的API路由

该模块定义了设备使用日志相关的FastAPI路由，包括记录使用、查询历史等功能。
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.usage_log import UsageLogCreate, UsageLogRead
from app.models.usage_log import UsageLog
from app.models.user import User
from app.database import get_db
from app.api.deps import get_current_user, get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/usage-logs", tags=["usage_logs"])

@router.post("/", response_model=UsageLogRead, summary="添加使用日志")
def create_usage_log(
    log_in: UsageLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建新的使用日志
    
    普通用户只能为自己创建日志
    管理员可以为任何用户创建日志
    """
    # 检查权限：普通用户只能为自己创建日志
    if current_user.role != "admin" and log_in.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权为其他用户创建日志"
        )
    
    # 创建日志
    db_log = UsageLog(**log_in.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/", response_model=List[UsageLogRead], summary="查询所有日志")
def read_usage_logs(
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    resource_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取使用日志列表
    
    普通用户只能查看自己的日志
    管理员可以查看所有日志，并可以按用户ID或资源类型过滤
    """
    # 构建查询
    query = db.query(UsageLog)
    
    # 权限检查和过滤条件
    if current_user.role != "admin":
        # 普通用户只能查看自己的日志
        query = query.filter(UsageLog.user_id == current_user.id)
    elif user_id:
        # 管理员可以按用户ID过滤
        query = query.filter(UsageLog.user_id == user_id)
    
    # 按资源类型过滤
    if resource_type:
        query = query.filter(UsageLog.resource_type == resource_type)
    
    # 分页
    logs = query.order_by(UsageLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/{log_id}", response_model=UsageLogRead, summary="查询日志详情")
def read_usage_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取特定使用日志详情
    
    普通用户只能查看自己的日志
    管理员可以查看所有日志
    """
    # 查询日志
    db_log = db.query(UsageLog).filter(UsageLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="日志不存在")
    
    # 权限检查
    if current_user.role != "admin" and db_log.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看其他用户的日志"
        )
    
    return db_log

@router.delete("/{log_id}", response_model=UsageLogRead, summary="删除日志")
def delete_usage_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    删除使用日志（仅管理员可用）
    """
    db_log = db.query(UsageLog).filter(UsageLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="日志不存在")
    
    db.delete(db_log)
    db.commit()
    return db_log
