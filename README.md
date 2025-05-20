# Lab-framework-core





## 后端基础服务启动说明

1. 进入 backend 目录：
   ```bash
   cd backend
   ```
2. 创建并激活 Python 虚拟环境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows 用户请使用 venv\Scripts\activate
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 启动 FastAPI 服务：
   ```bash
   uvicorn app.main:app --reload
   ```
5. 访问接口测试：
   - 打开浏览器访问 [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - 或访问自动生成的接口文档 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

如需关闭服务，按下 `Ctrl+C` 即可。


---

## 用户认证系统实现步骤与维护须知

### 1. 密码加密与校验工具
- 作用：保证用户密码安全，存储时只保存加密后的密码。
- 维护须知：如需更换加密算法，需同步修改注册和登录逻辑。
- 实现说明：
  - 使用 passlib 的 bcrypt 算法进行密码加密和校验。
  - 相关函数在 `backend/app/core/security.py` 中：
    - `get_password_hash(password)`：加密明文密码
    - `verify_password(plain, hashed)`：校验明文密码和哈希密码

### 2. JWT 生成与校验工具
- 作用：为登录用户生成令牌（Token），用于后续接口的身份校验。
- 维护须知：密钥和Token过期时间需妥善保管和配置，泄露会导致安全风险。
- 实现说明：
  - 使用 python-jose 生成和校验 JWT。
  - 相关函数在 `backend/app/core/security.py` 中：
    - `create_access_token(data, expires_delta)`：生成Token
    - `decode_access_token(token)`：校验并解析Token
  - `SECRET_KEY` 建议在生产环境中通过环境变量配置。

### 3. 用户注册与登录接口
- 作用：注册仅限管理员操作，普通用户不能自助注册。登录接口返回JWT Token。
- 维护须知：注册接口应校验当前用户权限，防止越权注册。

### 4. 用户相关API路由
- 作用：统一管理用户相关接口，便于维护和扩展。
- 维护须知：如需扩展用户功能（如重置密码、修改信息），建议在此目录下新增API。

### 5. 用户身份与权限依赖项
- 作用：用于API接口中自动获取当前用户、校验用户身份和权限。
- 维护须知：如需调整权限逻辑（如增加角色类型），需同步修改依赖项实现。
- 实现说明：
  - 相关依赖在 `backend/app/api/deps.py` 中：
    - `get_current_user`：通过JWT Token获取当前用户
    - `get_current_admin_user`：校验当前用户是否为管理员
  - 依赖项可在API接口参数中通过 `Depends` 注入。

### 6. 用户注册与登录接口说明
- 注册接口：`POST /api/register`
  - 仅管理员可用，需携带管理员Token。
  - 请求体：`UserCreate`（用户名、邮箱、密码、角色）
  - 返回：新建用户信息
- 登录接口：`POST /api/login`
  - 所有用户可用，使用表单（username, password）提交。
  - 返回：`access_token`（JWT Token），后续接口需在Header中携带 `Authorization: Bearer <token>`
- 维护须知：
  - 注册接口需校验当前用户权限，防止越权注册。
  - 登录接口返回的Token用于后续所有需要认证的接口。

### 7. 接口测试指南

#### 1. 启动后端服务
确保已按照前述步骤启动 FastAPI 服务。

#### 2. 创建初始管理员用户（首次建库时需手动插入）
由于注册接口仅限管理员，首次使用时需手动在数据库插入一条管理员用户记录。

以 SQLite 为例：
- 进入 Python 交互环境：
  ```bash
  cd backend
  source venv/bin/activate
  python
  ```
- 执行以下代码（需先 `pip install sqlalchemy`）：
  ```python
  from app.models.user import User, Base
  from app.core.security import get_password_hash
  from app.database import engine, SessionLocal
  Base.metadata.create_all(bind=engine)
  db = SessionLocal()
  admin = User(username="admin", email="admin@example.com", hashed_password=get_password_hash("admin123"), role="admin")
  db.add(admin)
  db.commit()
  db.close()
  exit()
  ```

#### 3. 管理员登录获取Token
```bash
curl -X POST "http://127.0.0.1:8000/api/login" -d 'username=admin&password=admin123' -H "Content-Type: application/x-www-form-urlencoded"
```
返回示例：
```json
{"access_token": "...", "token_type": "bearer"}
```

#### 4. 管理员添加新用户
```bash
curl -X POST "http://127.0.0.1:8000/api/register" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user1@example.com", "password": "userpass", "role": "user"}'
```

#### 5. 普通用户登录
```bash
curl -X POST "http://127.0.0.1:8000/api/login" -d 'username=user1&password=userpass' -H "Content-Type: application/x-www-form-urlencoded"
```

#### 6. 常见问题
- 注册接口返回 403：请确认使用的是管理员Token
- 登录接口返回 400：请检查用户名和密码是否正确
- 其他问题可通过 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 交互式文档测试

