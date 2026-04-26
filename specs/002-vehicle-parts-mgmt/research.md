# Research & Decisions: 整车零部件管理系统

## Decision 1: 数据库连接池配置

**Decision**: 使用 SQLAlchemy 异步引擎（`create_async_engine`）配合 `AsyncSession`，连接池大小 20，最大溢出 10。
**Rationale**: FastAPI 是异步框架，使用异步引擎避免线程阻塞。项目规模小（50 并发），20 连接池足够。
**Alternatives considered**:
- 同步引擎 + run_in_threadpool: 简单但与 FastAPI 异步特性不匹配
- ODBC (aiomysql): 性能更好但配置复杂，生态不如 pymysql

## Decision 2: JWT Token 过期策略

**Decision**: Access Token 有效期 24 小时（1440 分钟），HS256 算法。
**Rationale**: 企业内部系统，24 小时平衡安全性与用户体验。无需 refresh token 机制（简化实现，符合 2 周开发周期约束）。
**Alternatives considered**:
- 短 token (15min) + refresh token: 更安全但增加前端复杂度
- Session 认证: 不适合前后端分离架构

## Decision 3: 前端状态管理策略

**Decision**: Redux Toolkit 仅管理认证状态（token、user、roles），页面状态使用 React useState。
**Rationale**: 项目规模小，仅认证状态需要全局共享。过度使用 Redux 增加样板代码。
**Alternatives considered**:
- Context API: 简单但 devtools 支持弱
- Zustand: 轻量但引入额外依赖

## Decision 4: 数据库初始化流程

**Decision**: 本地 MySQL 已通过 Docker 运行。建表 SQL 直接执行，Alembic 仅用于后续变更。seed 脚本插入初始数据。
**Rationale**: 用户已明确本地 MySQL 可用。直接执行 SQL 最快速。
**Alternatives considered**:
- 纯 Alembic 迁移: 标准但需要首次配置
- SQLAlchemy create_all: 不适合生产环境

## Decision 5: 后端 CORS 配置

**Decision**: 开发环境允许 `http://localhost:5173`，生产环境限制为同域名。
**Rationale**: 开发时前后端不同端口，必须 CORS。生产环境通过 Nginx 同域代理。
**Alternatives considered**:
- 反向代理统一域名: 生产标准但开发不便
- JSONP: 过时且不安全

## Decision 6: 密码复杂度策略

**Decision**: 最小长度 6 位，无其他复杂度要求。bcrypt rounds=12。
**Rationale**: 企业内部系统，降低用户记忆负担。spec 已明确此假设。
**Alternatives considered**:
- 强制大小写+数字+特殊字符: 更安全但用户体验差

## Decision 7: Alembic 配置

**Decision**: `alembic.ini` 中 sqlalchemy.url 从 .env 读取，env.py 中使用 `config.get_main_option("sqlalchemy.url")`。
**Rationale**: 环境变量管理数据库连接，避免硬编码。
**Alternatives considered**:
- 硬编码 URL: 不安全
- 使用 alembic post-write hook 动态生成: 过度工程
