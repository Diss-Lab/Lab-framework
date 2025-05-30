from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/api", tags=["用户管理"])

# 管理员添加用户
@router.post(
    "/register",
    response_model=UserRead,
    summary="管理员添加用户 (临时修改：允许无认证注册)",
    description="临时修改：允许无认证注册，并将第一个用户设为管理员。完成后请改回！"
)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 检查是否是第一个用户，如果是，则强制设为 admin
    is_first_user = db.query(User).first() is None
    role = "admin" if is_first_user else (user_in.role or "user")

    if not is_first_user and db.query(User).filter((User.username == user_in.username) | (User.email == user_in.email)).first():
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")
    elif is_first_user and db.query(User).filter(User.username == user_in.username).first(): # 第一个用户只检查用户名
        raise HTTPException(status_code=400, detail="用户名已存在")


    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 用户登录
@router.post(
    "/login",
    summary="用户登录",
    description="输入用户名和密码，获取访问令牌。"
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
