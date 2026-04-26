# Implementation Plan: 整车零部件管理系统

**Branch**: `dev` | **Date**: 2026-04-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-vehicle-parts-mgmt/spec.md`

## Summary

构建企业内部后台管理系统，实现整车信息、零部件信息、装配关联关系及用户权限管理。
采用前后端分离架构：后端 FastAPI + SQLAlchemy + MySQL，前端 React 18 + Ant Design 5。
项目规模适合单人 2 周内完成，数据量预估：整车 ≤500、零部件 ≤5000、装配关系 ≤20000。

## Technical Context

**Language/Version**: Python 3.11 (后端), JavaScript ES2022 (前端)
**Primary Dependencies**: FastAPI, SQLAlchemy 2.x, Pydantic v2, pymysql, bcrypt, python-jose (JWT), Alembic, loguru | React 18, Vite, Ant Design 5, Redux Toolkit, Axios, ECharts
**Storage**: MySQL 8.x (本地 Docker, root/123456, 数据库名 vehicle_parts)
**Testing**: pytest + pytest-cov (后端), Vitest + React Testing Library (前端)
**Target Platform**: Linux/macOS 开发, 浏览器 Chrome 100+ / Edge 100+
**Project Type**: Web 应用（前后端分离）
**Performance Goals**: UI 响应 ≤100ms, API P95 ≤200ms, 列表页加载 ≤2s (500 条内)
**Constraints**: 单页 JS ≤200KB gzip, 数据库查询 ≤10 次/请求, N+1 查询视为 bug
**Scale/Scope**: 50 并发用户, 整车 ≤500, 零部件 ≤5000, 装配关系 ≤20000

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

All implementation plans must verify compliance with the project constitution
(.specify/memory/constitution.md). Key gates:

- **TDD Compliance**: ✅ 所有模块将先写测试后实现，pytest 覆盖 CRUD、认证、权限逻辑
- **Coverage Target**: ✅ 目标 ≥90% 行覆盖率 + ≥90% 分支覆盖率，CI 门禁拦截
- **Performance Budget**: ✅ UI ≤100ms 通过 Ant Design 组件优化实现；API ≤200ms 通过索引 + 聚合查询
- **UX Consistency**: ✅ 全部使用 Ant Design 5 组件，统一布局（MainLayout + Header + Content）
- **Complexity Justification**: ✅ 无额外复杂度，标准 CRUD + JWT 认证，无过度设计

## Project Structure

### Documentation (this feature)

```text
specs/002-vehicle-parts-mgmt/
├── spec.md              # 业务规格说明书
├── plan.md              # 实施规划（本文件）
├── tech-spec.md         # 技术设计文档（数据库 SQL、API 设计、目录结构）
├── research.md          # Phase 0 研究决策记录
├── data-model.md        # Phase 1 数据模型
├── quickstart.md        # Phase 1 快速启动指南
├── contracts/           # Phase 1 API 契约
│   └── api-contracts.json
└── tasks.md             # Phase 2 任务列表（由 /speckit-tasks 生成）
```

### Source Code (repository root)

```text
backend/
├── README.md
├── requirements.txt
├── .env.example
├── alembic.ini
├── alembic/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial_schema.py
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── deps.py
│   │   └── exceptions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── vehicle.py
│   │   ├── part.py
│   │   └── vehicle_part.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── vehicle.py
│   │   ├── part.py
│   │   └── vehicle_part.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── vehicle.py
│   │   ├── part.py
│   │   └── vehicle_part.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── dashboard_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── roles.py
│   │       ├── vehicles.py
│   │       ├── parts.py
│   │       ├── vehicle_parts.py
│   │       └── dashboard.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── response.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── scripts/
│   └── seed_data.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_auth.py
    ├── test_users.py
    ├── test_vehicles.py
    ├── test_parts.py
    └── test_vehicle_parts.py

frontend/
├── README.md
├── package.json
├── vite.config.js
├── index.html
├── .env.development
├── .env.production
├── public/
│   └── favicon.ico
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── assets/
    │   └── styles/
    │       └── global.css
    ├── api/
    │   ├── request.js
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
        ├── auth.js
        └── constants.js
```

**Structure Decision**: 采用 Option 2（前后端分离 Web 应用）结构。`backend/` 存放 FastAPI 项目，`frontend/` 存放 React + Vite 项目。两项目独立开发、独立部署，开发时通过 CORS + proxy 通信。

## Complexity Tracking

> 无宪法违规项。本项目为标准 CRUD + 权限管理，无额外复杂度需要证明。

---

## Phase 0: Research & Decisions

### Decision 1: 数据库连接池配置

**Decision**: 使用 SQLAlchemy 异步引擎（`create_async_engine`）配合 `AsyncSession`，连接池大小 20，最大溢出 10。
**Rationale**: FastAPI 是异步框架，使用异步引擎避免线程阻塞。本项目规模小，20 连接池足够支撑 50 并发。
**Alternatives considered**: 同步引擎（简单但与 FastAPI 异步特性不匹配）；ODBC（性能好但配置复杂）。

### Decision 2: JWT Token 过期策略

**Decision**: Access Token 有效期 24 小时（1440 分钟），使用 HS256 算法。
**Rationale**: 企业内部系统，24 小时平衡安全性与用户体验。无需 refresh token 机制（简化实现，符合 2 周开发周期约束）。
**Alternatives considered**: 短 token + refresh token（更安全但增加复杂度）；session 认证（不适合前后端分离）。

### Decision 3: 前端状态管理策略

**Decision**: Redux Toolkit 仅管理认证状态（token、user、roles），其余页面状态使用 React useState。
**Rationale**: 项目规模小，仅认证状态需要全局共享。过度使用 Redux 会增加样板代码。
**Alternatives considered**: 全局 Context API（简单但 devtools 支持弱）；Zustand（轻量但多一个依赖）。

### Decision 4: 数据库初始化流程

**Decision**: 本地 MySQL 已通过 Docker 运行。建表 SQL 直接执行（`mysql -u root -p123456 < init.sql`），Alembic 仅用于后续变更。seed 脚本插入初始角色和 admin 账户。
**Rationale**: 用户已明确本地 MySQL 可用。直接执行 SQL 最快速，Alembic 保留用于后续版本管理。
**Alternatives considered**: 纯 Alembic 迁移（标准但需要首次配置）；SQLAlchemy create_all（不适合生产）。

### Decision 5: 后端 CORS 配置

**Decision**: 开发环境允许 `http://localhost:5173`（Vite 默认端口）跨域，生产环境限制为同域名。
**Rationale**: 开发时前后端不同端口，必须 CORS。生产环境通过 Nginx 同域代理，无需宽泛 CORS。
**Alternatives considered**: 反向代理统一域名（生产标准但开发不便）；JSONP（过时）。

### Decision 6: 密码复杂度策略

**Decision**: 最小长度 6 位，无其他复杂度要求。bcrypt rounds=12。
**Rationale**: 企业内部系统，降低用户记忆负担。spec 中已明确此假设。
**Alternatives considered**: 强制大小写+数字+特殊字符（更安全但用户体验差）。

---

## Phase 1: Design & Contracts

### 1.1 Data Model (data-model.md)

数据模型详见 `data-model.md` 文件（下方生成）。

### 1.2 API Contracts

API 接口契约详见 `tech-spec.md` 第二部分。完整 JSON Schema 定义在 `contracts/` 目录。

### 1.3 Quickstart

快速启动指南详见 `quickstart.md` 文件（下方生成）。

---

## Complexity Tracking (Post-Design Re-evaluation)

设计阶段未发现需要额外复杂度的场景。标准 CRUD 架构满足所有功能需求。
