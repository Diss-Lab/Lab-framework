"""
用户相关的Pydantic模型

该模块定义了用户数据的Pydantic模型，用于数据验证、序列化和反序列化。
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 用户基础模型
class UserBase(BaseModel):
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="电子邮箱")

# 用户创建模型
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="用户密码，至少6个字符")
    role: str = Field("user", description="用户角色，默认为普通用户")

# 用户更新模型
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="电子邮箱")
    password: Optional[str] = Field(None, min_length=6, description="用户密码，至少6个字符")
    role: Optional[str] = Field(None, description="用户角色")

# 用户读取模型（从数据库返回的）
class UserRead(UserBase):
    id: int
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True  # 允许从ORM模型创建Pydantic模型
