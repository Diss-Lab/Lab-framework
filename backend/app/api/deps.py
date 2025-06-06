"""
API 依赖函数

这个模块定义了API路由中使用的各种依赖函数，如身份验证和权限检查等。
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    验证当前用户的函数依赖
    
    通过解析JWT令牌获取当前用户
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        if token_data.sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无法验证凭证",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无法验证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == token_data.sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    验证当前用户处于活跃状态的函数依赖
    """
    # 你可能有一个is_active字段，这里简化了实现
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    验证当前用户是否为管理员的函数依赖
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户权限不足，需要管理员权限"
        )
    return current_user
