from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.usage_log import Base as UsageLogBase
from app.models.user import Base as UserBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # 可根据需要更换为PostgreSQL等

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    UserBase.metadata.create_all(bind=engine)
    UsageLogBase.metadata.create_all(bind=engine)
