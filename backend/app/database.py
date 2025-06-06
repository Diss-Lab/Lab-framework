"""
数据库配置和会话管理模块

本模块提供了SQLAlchemy数据库的配置、连接和会话管理功能。
主要包含数据库URL配置、引擎创建、会话工厂设置以及数据库初始化等功能。

使用示例:
    from database import get_db, init_db
    
    # 初始化数据库表
    init_db()
    
    # 在FastAPI路由中使用数据库会话
    @app.get("/users/")
    def read_users(db: Session = Depends(get_db)):
        return db.query(User).all()
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库 URL (SQLite 文件路径)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# 如果使用 PostgreSQL 或其他数据库，URL 格式会不同

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建所有模型的基类
Base = declarative_base()

def get_db():
    """
    创建数据库会话的依赖函数
    
    yields:
        Session: 数据库会话对象
        
    使用方式:
        在FastAPI路由函数中通过Depends(get_db)注入会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    初始化数据库表结构
    
    根据模型定义创建用户表和使用日志表
    如果表已存在，则不会重复创建
    """
    # 导入所有模型以确保它们被注册到 Base.metadata
    from app.models import user, usage_log
    Base.metadata.create_all(bind=engine)

def create_tables():
    """
    创建数据库表

    根据当前模型的定义创建所有表。如果表已经存在，则不会重复创建。
    通常在应用启动时调用一次。
    """
    Base.metadata.create_all(bind=engine)