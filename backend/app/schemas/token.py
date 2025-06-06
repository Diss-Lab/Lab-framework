"""
认证相关的Pydantic模型

该模块定义了身份验证和授权相关的Pydantic模型。
"""

from pydantic import BaseModel
from typing import Optional

# 令牌响应模型
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# 令牌数据模型
class TokenPayload(BaseModel):
    sub: Optional[str] = None  # 主题（通常是用户ID或用户名）
