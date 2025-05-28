"""
实验室管理系统 API 服务

本模块实现了实验室管理系统的主要 API 服务，提供用户管理、使用记录等功能。
使用 FastAPI 框架构建，支持异步操作，提供 OpenAPI 文档。

主要功能：
- 用户管理 API
- 使用记录管理 API
- CORS 跨域支持
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, usage_logs

# 创建 FastAPI 应用实例
# 配置应用基本信息，包括标题、描述和版本号
# 这些信息将显示在自动生成的 API 文档中
app = FastAPI(
    title="实验室管理系统 API",
    description="本系统用于实验室用户、设备、材料、数据的统一管理。",
    version="1.0.0"
)

# CORS（跨源资源共享）中间件配置
# 开发环境下允许所有来源访问API
# allow_origins: 允许的源列表
# allow_credentials: 允许携带认证信息
# allow_methods: 允许的 HTTP 方法
# allow_headers: 允许的 HTTP 头
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由模块
# users: 用户相关的路由处理器
# usage_logs: 使用记录相关的路由处理器
app.include_router(users.router)
app.include_router(usage_logs.router)

# API 根路径
# 返回欢迎信息
# 方法: GET
# 路径: /
@app.get("/")
async def root():
    return {"message": "欢迎使用实验室管理系统 API"}