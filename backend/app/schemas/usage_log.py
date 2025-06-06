"""
使用日志相关的Pydantic模型

该模块定义了使用日志数据的Pydantic模型，用于数据验证、序列化和反序列化。
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 使用日志基础模型
class UsageLogBase(BaseModel):
    resource_type: str
    resource_id: int
    action: str
    quantity_used: Optional[float] = None
    duration_minutes: Optional[int] = None
    purpose: Optional[str] = None
    notes: Optional[str] = None
    issues_reported: Optional[str] = None
    project_name: Optional[str] = None

# 使用日志创建模型
class UsageLogCreate(UsageLogBase):
    user_id: int
    auto_recorded: bool = False
    
# 使用日志读取模型
class UsageLogRead(UsageLogBase):
    id: int
    user_id: int
    timestamp: datetime
    auto_recorded: bool
    
    class Config:
        from_attributes = True
