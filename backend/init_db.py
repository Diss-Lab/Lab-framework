from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.database import SQLALCHEMY_DATABASE_URL
from app.models.user import User
from app.models.usage_log import UsageLog

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 创建 Base 类 - 所有 SQLAlchemy 模型的基类
Base = declarative_base()

def init_db():
    print("正在初始化数据库...")
    
    # 创建所有表
    # 注意：这会创建表，但不会修改现有表结构
    Base.metadata.create_all(bind=engine)
    
    print("数据库表创建完成！")
    
    # 创建示例数据（可选）
    # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # db = SessionLocal()
    # try:
    #     # 添加示例数据的代码
    #     pass
    # finally:
    #     db.close()

if __name__ == "__main__":
    init_db()
