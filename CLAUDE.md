# 整车零部件管理系统（Vehicle Parts Management System）

> 本文档为 AI 编码工具的主要上下文文件。详细规格见 `specs/002-vehicle-parts-mgmt/`
> 实施规划: [specs/002-vehicle-parts-mgmt/plan.md](specs/002-vehicle-parts-mgmt/plan.md)

## 项目概述

企业内部后台管理系统，实现整车信息、零部件信息、整车零部件装配关联关系及用户权限管理。
适合单人 2 周内开发完成。

## 技术栈

| 层 | 技术 |
|----|------|
| 后端 | Python 3.11 + FastAPI + SQLAlchemy 2.x + Pydantic + MySQL 8.x |
| 认证 | JWT Token + bcrypt |
| 迁移 | Alembic |
| 日志 | loguru |
| 前端 | React 18 + Vite + Ant Design 5 + React Router DOM + Redux Toolkit + Axios + Echarts |

## 项目目录

### 后端 (backend/)

```
backend/
├── requirements.txt
├── .env.example
├── alembic.ini
├── alembic/
│   └── versions/
│       └── 001_initial_schema.py
└── app/
    ├── main.py                      # FastAPI 应用入口
    ├── core/
    │   ├── config.py                # 配置管理
    │   ├── security.py              # JWT + 密码加密
    │   ├── deps.py                  # 依赖注入
    │   └── exceptions.py            # 异常处理
    ├── models/
    │   ├── base.py                  # SQLAlchemy 基类
    │   ├── user.py                  # SysUser
    │   ├── role.py                  # SysRole
    │   ├── vehicle.py               # VehicleInfo
    │   ├── part.py                  # PartInfo
    │   └── vehicle_part.py          # VehiclePartRelation
    ├── schemas/
    │   ├── common.py                # Result, PageResponse
    │   ├── auth.py
    │   ├── user.py
    │   ├── role.py
    │   ├── vehicle.py
    │   ├── part.py
    │   └── vehicle_part.py
    ├── crud/
    │   ├── base.py                  # 泛型 CRUD 基类
    │   ├── user.py
    │   ├── role.py
    │   ├── vehicle.py
    │   ├── part.py
    │   └── vehicle_part.py
    ├── services/
    │   ├── auth_service.py
    │   ├── user_service.py
    │   └── dashboard_service.py
    ├── api/
    │   ├── router.py
    │   └── v1/
    │       ├── auth.py
    │       ├── users.py
    │       ├── roles.py
    │       ├── vehicles.py
    │       ├── parts.py
    │       ├── vehicle_parts.py
    │       └── dashboard.py
    ├── utils/
    │   └── response.py
    └── config/
        └── settings.py
```

### 前端 (frontend/)

```
frontend/
├── package.json
├── vite.config.js
├── index.html
├── .env.development
├── .env.production
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── api/
    │   ├── request.js               # Axios 封装
    │   ├── auth.js
    │   ├── user.js
    │   ├── role.js
    │   ├── vehicle.js
    │   ├── part.js
    │   ├── vehiclePart.js
    │   └── dashboard.js
    ├── store/
    │   ├── index.js
    │   └── slices/
    │       ├── authSlice.js
    │       └── appSlice.js
    ├── components/
    │   ├── Layout/
    │   │   ├── MainLayout.jsx
    │   │   └── Header.jsx
    │   ├── SearchForm/
    │   │   └── index.jsx
    │   └── DataTable/
    │       └── index.jsx
    ├── pages/
    │   ├── Login/index.jsx
    │   ├── Dashboard/index.jsx
    │   ├── UserManage/index.jsx
    │   ├── RoleManage/index.jsx
    │   ├── VehicleManage/index.jsx
    │   ├── PartManage/index.jsx
    │   ├── RelationManage/index.jsx
    │   └── ProfilePassword/index.jsx
    ├── router/
    │   ├── index.js
    │   └── routes.js
    └── utils/
        ├── auth.js                  # Token localStorage 管理
        └── constants.js
```

## 数据库表

| 表名 | 说明 |
|------|------|
| sys_user | 用户表 |
| sys_role | 角色表（仅 admin / viewer） |
| sys_user_role | 用户角色关联表 |
| vehicle_info | 整车信息表 |
| part_info | 零部件信息表 |
| vehicle_part_relation | 装配关系表 |

详细建表 SQL 见 `specs/002-vehicle-parts-mgmt/tech-spec.md`

## API 接口

| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| 认证 | /api/auth | 登录、用户信息、改密码 |
| 用户 | /api/users | CRUD + 状态 + 角色分配 |
| 角色 | /api/roles | 查询 |
| 整车 | /api/vehicles | CRUD + 详情 |
| 零部件 | /api/parts | CRUD + 详情 |
| 装配 | /api/relations, /api/vehicles/{id}/parts, /api/parts/{id}/vehicles | CRUD + BOM + 引用 |
| 统计 | /api/dashboard/statistics | 首页卡片 + 图表数据 |

所有接口返回统一格式：`{ "code": 200, "message": "success", "data": ... }`

完整接口设计见 `specs/002-vehicle-parts-mgmt/tech-spec.md`

## 权限规则

- **admin**: 全部增删改查权限
- **viewer**: 仅查看权限

viewer 不可见的按钮：所有新增、编辑、删除、停用操作按钮

## 代码生成约束

1. 数据库实体字段命名 = API 字段名 = 前端表单字段名（全部 snake_case）
2. 所有 CRUD 页面必须包含新增/编辑/删除/详情功能
3. 所有列表页面必须支持分页
4. 所有查询必须支持条件筛选 + 重置按钮
5. 新增/编辑共用 Modal 弹窗
6. 前端 Axios 统一封装 request.ts，自动附加 Token
7. Token 存储在 localStorage
8. 左侧后台菜单布局
9. 库存预警：stock_qty < safe_stock 时标记

## 项目原则（宪法）

详见 `.specify/memory/constitution.md`：
- TDD 驱动开发，覆盖率 ≥ 90%
- UI 响应时间 ≤ 100ms
- 代码质量标准（lint 零警告）
- 用户体验一致性
