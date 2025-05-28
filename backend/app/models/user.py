"""
用户模型模块

该模块定义了系统中用户相关的数据模型，包括用户基本信息、认证信息和角色信息。
使用SQLAlchemy ORM框架进行数据库映射。

使用示例:
    from app.models.user import User
    
    # 创建新用户
    new_user = User(
        username="john_doe",
        email="john@example.com",
        hashed_password="xxx",
        role="user"
    )
    
    # 数据库操作
    db.session.add(new_user)
    db.session.commit()
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.models.usage_log import Base  # 保证Base一致

class User(Base):
    """用户模型类
    
    该类定义了用户的数据结构，包含用户的基本信息、认证信息等。
    继承自SQLAlchemy的Base类，映射到数据库的users表。
    """
    
    __tablename__ = "users"  # 数据库表名

    # 用户唯一标识ID
    id = Column(Integer, primary_key=True, index=True)
    
    # 用户名，唯一且必填，建立索引以提高查询性能
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # 电子邮箱，唯一且必填，建立索引以提高查询性能
    email = Column(String(100), unique=True, index=True, nullable=False)
    
    # 密码哈希值，必填，存储加密后的密码
    hashed_password = Column(String(128), nullable=False)
    
    # 用户角色，默认为"user"，用于权限控制
    role = Column(String(20), default="user")
    
    # 用户创建时间，默认为当前UTC时间
    created_at = Column(DateTime, default=datetime.datetime.utcnow)