# Quickstart: 整车零部件管理系统

## 前置条件

- Python 3.11+
- Node.js 18+
- MySQL 8.x (本地 Docker 运行，root/123456)
- 数据库 `vehicle_parts` 已创建并执行建表 SQL

## 后端启动

```bash
cd backend

# 1. 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env: DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/vehicle_parts?charset=utf8mb4
#          SECRET_KEY=your-secret-key-change-in-production

# 4. 初始化数据库（如果尚未建表）
# mysql -u root -p123456 vehicle_parts < scripts/init.sql

# 5. 插入初始数据（角色 + admin 账户）
python scripts/seed_data.py

# 6. 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端地址: http://localhost:8000
Swagger 文档: http://localhost:8000/docs

## 前端启动

```bash
cd frontend

# 1. 安装依赖
npm install

# 2. 配置环境变量（.env.development 已包含默认值）
# VITE_API_BASE_URL=http://localhost:8000

# 3. 启动开发服务器
npm run dev
```

前端地址: http://localhost:5173

## 默认账户

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 超级管理员 |

> 首次登录后建议修改默认密码。

## 验证清单

- [ ] 后端 /docs 页面可访问
- [ ] 前端登录页可访问
- [ ] 使用 admin/admin123 登录成功
- [ ] 首页显示统计数据
- [ ] 可以新增一辆整车
- [ ] 可以新增一个零部件
- [ ] 可以为整车添加装配关系
