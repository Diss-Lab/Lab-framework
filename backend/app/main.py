from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users

app = FastAPI(
    title="实验室管理系统 API",
    description="本系统用于实验室用户、设备、材料、数据的统一管理。",
    version="1.0.0"
)

# 配置CORS，允许所有来源（开发阶段）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "欢迎使用实验室管理系统 API"}
