from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "user"
    
    class Config:
        # 修改 orm_mode 为 from_attributes，适配 Pydantic V2
        from_attributes = True  # 替换原来的 orm_mode = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    
    class Config:
        # 确保这里也使用 from_attributes
        from_attributes = True

class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True  # 替换 orm_mode = True
