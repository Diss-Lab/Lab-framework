from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True
