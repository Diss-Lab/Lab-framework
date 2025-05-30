from sqlalchemy.orm import Session
from app.database import SessionLocal, engine # 假设你的 database.py 中有 SessionLocal 和 engine
from app.models.user import User # 确保 User 模型已定义表结构
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

# 如果 User 模型还没有创建表，需要先创建
# User.metadata.create_all(bind=engine) # 取消注释这行如果表还没创建

def create_admin_user():
    db: Session = SessionLocal()
    try:
        admin_username = "scriptadmin"
        admin_email = "scriptadmin@example.com"
        admin_password = "supersecurepassword" # 设置一个强密码

        existing_admin = db.query(User).filter(User.username == admin_username).first()
        if existing_admin:
            print(f"User {admin_username} already exists.")
            return

        hashed_password = get_password_hash(admin_password)
        admin_user = User(
            username=admin_username,
            email=admin_email,
            hashed_password=hashed_password,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"Admin user {admin_user.username} created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    print("Attempting to create admin user...")
    # 确保 User 表已在数据库中创建
    # 如果你的 User 模型定义中包含 Base = declarative_base()
    # 并且你的 database.py 或 main.py 中有 Base.metadata.create_all(bind=engine)
    # 那么表应该已经创建了。如果没有，你可能需要在这里调用它。
    # from app.models.user import Base # 假设 Base 在这里
    # Base.metadata.create_all(bind=engine)

    create_admin_user()
