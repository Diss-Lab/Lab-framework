"""
FastAPI应用程序入口

此模块初始化FastAPI应用程序，配置数据库连接，设置中间件，
并包含API路由设置。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db, create_tables
from app.api import users, usage_logs

# 初始化FastAPI应用
app = FastAPI(
    title="实验室管理系统",
    description="实验室设备和资源管理系统API",
    version="0.1.0",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库表
create_tables()
# 或者使用 init_db() 两者都可以

# 包含API路由
app.include_router(users.router, prefix="/api")
app.include_router(usage_logs.router, prefix="/api")

@app.get("/")
def root():
    """
    根路由，返回API欢迎信息
    """
    return {
        "message": "欢迎使用实验室管理系统API",
        "documentation": "/docs",
    }