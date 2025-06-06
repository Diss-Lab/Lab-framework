"""
用户相关的API路由

该模块定义了用户管理相关的FastAPI路由，包括用户注册、登录、查询等功能。
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.token import Token
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.database import get_db
from app.api.deps import get_current_user, get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserRead)
def register_user(
    user_in: UserCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_admin_user)
):
    """
    创建新用户（仅管理员可用）
    """
    # 检查用户名是否已存在
    user_by_username = db.query(User).filter(User.username == user_in.username).first()
    if user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被注册"
        )
    
    # 检查邮箱是否已存在
    user_by_email = db.query(User).filter(User.email == user_in.email).first()
    if user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    # 创建新用户
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    用户登录获取令牌
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    获取当前登录用户信息
    """
    return current_user

@router.get("/", response_model=List[UserRead])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_admin_user)
):
    """
    获取所有用户列表（仅管理员可用）
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    更新用户信息（仅管理员可用）
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新用户信息
    if user_in.email:
        db_user.email = user_in.email
    if user_in.password:
        db_user.hashed_password = get_password_hash(user_in.password)
    if user_in.role:
        db_user.role = user_in.role
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=UserRead)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    删除用户（仅管理员可用）
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db.delete(db_user)
    db.commit()
    return db_user
