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
from sqlalchemy.orm import sessionmaker

from app.models.usage_log import Base as UsageLogBase
from app.models.user import Base as UserBase

# 数据库连接配置
# 当前使用SQLite数据库，数据库文件位于当前目录的test.db
# 可以通过修改此URL切换到其他数据库（如PostgreSQL、MySQL等）
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # 可根据需要更换为PostgreSQL等

# 创建数据库引擎
# connect_args={'check_same_thread': False} 是SQLite特有的设置
# 允许多线程访问数据库，生产环境中使用其他数据库时可以移除此参数
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建会话工厂
# autocommit=False: 不自动提交事务
# autoflush=False: 不自动刷新session
# bind=engine: 绑定到上面创建的数据库引擎
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    UserBase.metadata.create_all(bind=engine)
    UsageLogBase.metadata.create_all(bind=engine)