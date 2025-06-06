from pydantic import BaseModel, EmailStr
from typing import Optional

# 令牌模型
class Token(BaseModel):
    access_token: str
    token_type: str

# 令牌载荷
class TokenPayload(BaseModel):
    sub: Optional[str] = None

# 用户基础模型
class UserBase(BaseModel):
    username: str
    email: EmailStr

# 用户创建模型（包含密码）
class UserCreate(UserBase):
    password: str
    role: str = "user"  # 默认为普通用户

# 用户信息输出模型
class UserOut(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True  # 允许从ORM模型创建Pydantic模型 (之前叫orm_mode)
