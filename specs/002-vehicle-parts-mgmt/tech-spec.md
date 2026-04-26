# 整车零部件管理系统 - 技术设计文档

> 本文档为 AI 编码工具（Claude Code / Cursor / Windsurf）提供可直接用于生成代码的详细技术规格。
> 与 `spec.md` 配套使用，`spec.md` 定义业务需求，本文定义技术实现。

---

## 一、数据库设计

### 1.1 ER 关系图

```
sys_user          sys_user_role          sys_role
┌─────────┐      ┌──────────────────┐    ┌─────────┐
│ id (PK) │◄─────│ user_id  (FK)    │    │ id (PK) │
│ username│      │ role_id  (FK)    │───►│role_name│
│ ...     │      └──────────────────┘    │ ...     │
└─────────┘                              └─────────┘

vehicle_info       vehicle_part_relation       part_info
┌──────────────┐  ┌───────────────────────┐   ┌────────────┐
│ id (PK)      │◄─│ vehicle_id (FK)       │   │ id (PK)    │
│ vehicle_code │  │ part_id    (FK)       │──►│ part_code  │
│ ...          │  │ quantity              │   │ ...        │
└──────────────┘  │ position_name         │   └────────────┘
                  │ remark                │
                  └───────────────────────┘
```

### 1.2 建表 SQL

```sql
-- ============================================
-- 1. sys_role 角色表
-- ============================================
CREATE TABLE `sys_role` (
  `id`          INT UNSIGNED    NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `role_name`   VARCHAR(32)     NOT NULL                COMMENT '角色名称: admin / viewer',
  `role_desc`   VARCHAR(128)    NOT NULL DEFAULT ''     COMMENT '角色描述',
  `create_time` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_role_name` (`role_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统角色表';

-- 初始化两个固定角色
INSERT INTO `sys_role` (`role_name`, `role_desc`) VALUES
  ('admin', '超级管理员，拥有全部增删改查权限'),
  ('viewer', '普通用户，仅拥有查看权限');

-- ============================================
-- 2. sys_user 用户表
-- ============================================
CREATE TABLE `sys_user` (
  `id`          INT UNSIGNED    NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username`    VARCHAR(64)     NOT NULL                COMMENT '用户名（登录用）',
  `real_name`   VARCHAR(64)     NOT NULL DEFAULT ''     COMMENT '真实姓名',
  `password`    VARCHAR(128)    NOT NULL                COMMENT '密码（bcrypt加密）',
  `phone`       VARCHAR(20)     NOT NULL DEFAULT ''     COMMENT '手机号',
  `email`       VARCHAR(128)    NOT NULL DEFAULT ''     COMMENT '邮箱',
  `status`      TINYINT         NOT NULL DEFAULT 1      COMMENT '状态: 1=启用, 0=停用',
  `is_deleted`  TINYINT         NOT NULL DEFAULT 0      COMMENT '软删除: 0=正常, 1=已删除',
  `create_time` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  KEY `idx_status` (`status`),
  KEY `idx_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统用户表';

-- ============================================
-- 3. sys_user_role 用户角色关联表
-- ============================================
CREATE TABLE `sys_user_role` (
  `id`          INT UNSIGNED    NOT NULL AUTO_INCREMENT COMMENT '关联ID',
  `user_id`     INT UNSIGNED    NOT NULL                COMMENT '用户ID',
  `role_id`     INT UNSIGNED    NOT NULL                COMMENT '角色ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_role` (`user_id`, `role_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_role_id` (`role_id`),
  CONSTRAINT `fk_ur_user` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_ur_role` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';

-- ============================================
-- 4. vehicle_info 整车信息表
-- ============================================
CREATE TABLE `vehicle_info` (
  `id`            INT UNSIGNED    NOT NULL AUTO_INCREMENT COMMENT '整车ID',
  `vehicle_code`  VARCHAR(64)     NOT NULL                COMMENT '整车编号（唯一）',
  `vehicle_name`  VARCHAR(128)    NOT NULL                COMMENT '整车名称',
  `vehicle_model` VARCHAR(128)    NOT NULL DEFAULT ''     COMMENT '整车型号',
  `brand`         VARCHAR(64)     NOT NULL DEFAULT ''     COMMENT '品牌',
  `year_model`    VARCHAR(16)     NOT NULL DEFAULT ''     COMMENT '年款',
  `engine_model`  VARCHAR(128)    NOT NULL DEFAULT ''     COMMENT '发动机型号',
  `description`   TEXT            NOT NULL DEFAULT ''     COMMENT '描述',
  `is_deleted`    TINYINT         NOT NULL DEFAULT 0      COMMENT '软删除: 0=正常, 1=已删除',
  `create_time`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_vehicle_code` (`vehicle_code`),
  KEY `idx_vehicle_name` (`vehicle_name`),
  KEY `idx_brand` (`brand`),
  KEY `idx_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='整车信息表';

-- ============================================
-- 5. part_info 零部件信息表
-- ============================================
CREATE TABLE `part_info` (
  `id`          INT UNSIGNED    NOT NULL AUTO_INCREMENT COMMENT '零部件ID',
  `part_code`   VARCHAR(64)     NOT NULL                COMMENT '零件编号（唯一）',
  `part_name`   VARCHAR(128)    NOT NULL                COMMENT '零件名称',
  `category`    VARCHAR(64)     NOT NULL DEFAULT ''     COMMENT '零件类别',
  `spec_model`  VARCHAR(128)    NOT NULL DEFAULT ''     COMMENT '规格型号',
  `material`    VARCHAR(128)    NOT NULL DEFAULT ''     COMMENT '材质',
  `supplier`    VARCHAR(128)    NOT NULL DEFAULT ''     COMMENT '供应商',
  `unit`        VARCHAR(16)     NOT NULL DEFAULT ''     COMMENT '单位',
  `price`       DECIMAL(10,2)   NOT NULL DEFAULT 0.00   COMMENT '单价（元）',
  `stock_qty`   INT             NOT NULL DEFAULT 0      COMMENT '库存数量',
  `safe_stock`  INT             NOT NULL DEFAULT 0      COMMENT '安全库存',
  `description` TEXT            NOT NULL DEFAULT ''     COMMENT '描述',
  `is_deleted`  TINYINT         NOT NULL DEFAULT 0      COMMENT '软删除: 0=正常, 1=已删除',
  `create_time` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_part_code` (`part_code`),
  KEY `idx_part_name` (`part_name`),
  KEY `idx_category` (`category`),
  KEY `idx_supplier` (`supplier`),
  KEY `idx_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='零部件信息表';

-- ============================================
-- 6. vehicle_part_relation 整车零部件装配关系表
-- ============================================
CREATE TABLE `vehicle_part_relation` (
  `id`            INT UNSIGNED    NOT NULL AUTO_INCREMENT COMMENT '关联ID',
  `vehicle_id`    INT UNSIGNED    NOT NULL                COMMENT '整车ID',
  `part_id`       INT UNSIGNED    NOT NULL                COMMENT '零部件ID',
  `quantity`      INT             NOT NULL DEFAULT 1      COMMENT '装配数量',
  `position_name` VARCHAR(128)    NOT NULL DEFAULT ''     COMMENT '装配位置',
  `remark`        VARCHAR(256)    NOT NULL DEFAULT ''     COMMENT '备注',
  `create_time`   DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_vehicle_part` (`vehicle_id`, `part_id`),
  KEY `idx_vehicle_id` (`vehicle_id`),
  KEY `idx_part_id` (`part_id`),
  CONSTRAINT `fk_vpr_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle_info` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_vpr_part`    FOREIGN KEY (`part_id`)    REFERENCES `part_info` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='整车零部件装配关系表';
```

### 1.3 索引策略

| 表名 | 索引 | 类型 | 用途 |
|------|------|------|------|
| sys_user | uk_username | UNIQUE | 登录查询、唯一约束 |
| sys_user | idx_status | NORMAL | 状态过滤 |
| sys_role | uk_role_name | UNIQUE | 角色名称唯一 |
| vehicle_info | uk_vehicle_code | UNIQUE | 编号唯一 |
| vehicle_info | idx_vehicle_name | NORMAL | 名称搜索 |
| vehicle_info | idx_brand | NORMAL | 品牌搜索 |
| part_info | uk_part_code | UNIQUE | 编号唯一 |
| part_info | idx_part_name | NORMAL | 名称搜索 |
| part_info | idx_category | NORMAL | 类别搜索 |
| part_info | idx_supplier | NORMAL | 供应商搜索 |
| vehicle_part_relation | uk_vehicle_part | UNIQUE | 防止重复装配 |
| vehicle_part_relation | idx_vehicle_id | NORMAL | 按整车查询BOM |
| vehicle_part_relation | idx_part_id | NORMAL | 按零件查引用整车 |

---

## 二、后端 RESTful API 设计

### 2.1 统一响应格式

所有接口统一返回以下 JSON 结构：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

分页列表返回：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 10
  }
}
```

错误返回：

```json
{
  "code": 400,
  "message": "错误描述信息",
  "data": null
}
```

### 2.2 认证接口

#### POST /api/auth/login - 用户登录

**请求体**:
```json
{
  "username": "admin",
  "password": "123456"
}
```

**返回**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "Bearer"
  }
}
```

#### GET /api/auth/userinfo - 获取当前用户信息

**请求头**: `Authorization: Bearer <token>`

**返回**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "admin",
    "real_name": "管理员",
    "phone": "13800138000",
    "email": "admin@example.com",
    "roles": ["admin"],
    "status": 1,
    "create_time": "2026-04-26T10:00:00"
  }
}
```

#### PUT /api/auth/change-password - 修改密码

**请求体**:
```json
{
  "old_password": "123456",
  "new_password": "654321"
}
```

**返回**:
```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": null
}
```

### 2.3 用户管理接口

#### GET /api/users - 分页查询用户列表

**查询参数**: `page=1&page_size=10&username=&real_name=`

**返回**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "username": "admin",
        "real_name": "管理员",
        "phone": "13800138000",
        "email": "admin@example.com",
        "roles": ["admin"],
        "status": 1,
        "create_time": "2026-04-26T10:00:00",
        "update_time": "2026-04-26T10:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10
  }
}
```

#### POST /api/users - 新增用户

**请求体**:
```json
{
  "username": "zhangsan",
  "real_name": "张三",
  "password": "123456",
  "phone": "13800138001",
  "email": "zhangsan@example.com",
  "role_ids": [2]
}
```

**返回**: 创建成功的用户对象

#### PUT /api/users/{id} - 编辑用户

**请求体**:
```json
{
  "real_name": "张三三",
  "phone": "13800138002",
  "email": "newemail@example.com",
  "role_ids": [2],
  "status": 1
}
```

#### DELETE /api/users/{id} - 删除用户（软删除）

#### PUT /api/users/{id}/status - 启用/停用用户

**请求体**: `{"status": 0}` (0=停用, 1=启用)

### 2.4 角色接口

#### GET /api/roles - 查询角色列表

**返回**:
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {"id": 1, "role_name": "admin", "role_desc": "超级管理员，拥有全部增删改查权限"},
    {"id": 2, "role_name": "viewer", "role_desc": "普通用户，仅拥有查看权限"}
  ]
}
```

### 2.5 整车接口

#### GET /api/vehicles - 分页查询整车列表

**查询参数**: `page=1&page_size=10&vehicle_code=&vehicle_name=&brand=`

**返回**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "vehicle_code": "VH-001",
        "vehicle_name": "Model S",
        "vehicle_model": "MS2024",
        "brand": "Tesla",
        "year_model": "2024",
        "engine_model": "Electric-AWD",
        "description": "纯电动轿车",
        "create_time": "2026-04-26T10:00:00",
        "update_time": "2026-04-26T10:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10
  }
}
```

#### POST /api/vehicles - 新增整车

**请求体**:
```json
{
  "vehicle_code": "VH-002",
  "vehicle_name": "Model 3",
  "vehicle_model": "M32024",
  "brand": "Tesla",
  "year_model": "2024",
  "engine_model": "Electric-RWD",
  "description": "纯电动中型轿车"
}
```

#### PUT /api/vehicles/{id} - 编辑整车

#### DELETE /api/vehicles/{id} - 删除整车

#### GET /api/vehicles/{id} - 查看整车详情

### 2.6 零部件接口

#### GET /api/parts - 分页查询零部件列表

**查询参数**: `page=1&page_size=10&part_code=&part_name=&category=&supplier=`

**返回**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "part_code": "PRT-001",
        "part_name": "前制动盘",
        "category": "制动系统",
        "spec_model": "BREM-320",
        "material": "铸铁",
        "supplier": "Brembo",
        "unit": "个",
        "price": 350.00,
        "stock_qty": 50,
        "safe_stock": 100,
        "low_stock": true,
        "description": "前轮制动盘",
        "create_time": "2026-04-26T10:00:00",
        "update_time": "2026-04-26T10:00:00"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10
  }
}
```

> `low_stock` 字段：当 `stock_qty < safe_stock` 时为 `true`，前端据此标记预警。

#### POST /api/parts - 新增零部件

#### PUT /api/parts/{id} - 编辑零部件

#### DELETE /api/parts/{id} - 删除零部件

#### GET /api/parts/{id} - 查看零部件详情

### 2.7 装配关系接口

#### GET /api/relations - 分页查询装配关系列表

**查询参数**: `page=1&page_size=10&vehicle_id=&part_id=`

#### POST /api/relations - 新增装配关系

**请求体**:
```json
{
  "vehicle_id": 1,
  "part_id": 1,
  "quantity": 2,
  "position_name": "左前轮",
  "remark": "标配"
}
```

#### PUT /api/relations/{id} - 编辑装配关系

#### DELETE /api/relations/{id} - 删除装配关系

#### GET /api/vehicles/{vehicle_id}/parts - 查看整车BOM清单

**返回**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "vehicle": {"id": 1, "vehicle_code": "VH-001", "vehicle_name": "Model S"},
    "parts": [
      {
        "relation_id": 1,
        "part_id": 1,
        "part_code": "PRT-001",
        "part_name": "前制动盘",
        "category": "制动系统",
        "quantity": 2,
        "position_name": "左前轮",
        "remark": "标配"
      }
    ],
    "total_parts": 1
  }
}
```

#### GET /api/parts/{part_id}/vehicles - 查看零部件被哪些整车引用

**返回**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "part": {"id": 1, "part_code": "PRT-001", "part_name": "前制动盘"},
    "vehicles": [
      {
        "relation_id": 1,
        "vehicle_id": 1,
        "vehicle_code": "VH-001",
        "vehicle_name": "Model S",
        "quantity": 2,
        "position_name": "左前轮"
      }
    ],
    "total_vehicles": 1
  }
}
```

### 2.8 首页统计接口

#### GET /api/dashboard/statistics - 首页统计

**返回**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "vehicle_count": 50,
    "part_count": 200,
    "user_count": 5,
    "low_stock_count": 3,
    "category_stats": [
      {"category": "制动系统", "count": 30},
      {"category": "发动机", "count": 45},
      {"category": "电气系统", "count": 55},
      {"category": "车身覆盖", "count": 25},
      {"category": "底盘", "count": 45}
    ],
    "low_stock_parts": [
      {"part_code": "PRT-001", "part_name": "前制动盘", "stock_qty": 50, "safe_stock": 100},
      {"part_code": "PRT-015", "part_name": "火花塞", "stock_qty": 10, "safe_stock": 50},
      {"part_code": "PRT-032", "part_name": "空气滤芯", "stock_qty": 5, "safe_stock": 30}
    ],
    "recent_vehicles": [
      {"id": 50, "vehicle_code": "VH-050", "vehicle_name": "新车50", "brand": "Brand", "create_time": "2026-04-26T09:00:00"}
    ],
    "recent_parts": [
      {"id": 200, "part_code": "PRT-200", "part_name": "新零件200", "category": "电气系统", "create_time": "2026-04-26T08:00:00"}
    ]
  }
}
```

### 2.9 权限拦截规则

| 接口路径 | admin | viewer |
|----------|-------|--------|
| GET /api/auth/* | ✓ | ✓ |
| POST /api/auth/login | ✓ | ✓ |
| GET /api/users | ✓ | ✗ |
| POST /api/users | ✓ | ✗ |
| PUT /api/users/{id} | ✓ | ✗ |
| DELETE /api/users/{id} | ✓ | ✗ |
| PUT /api/users/{id}/status | ✓ | ✗ |
| GET /api/roles | ✓ | ✗ |
| GET /api/vehicles | ✓ | ✓ |
| POST /api/vehicles | ✓ | ✗ |
| PUT /api/vehicles/{id} | ✓ | ✗ |
| DELETE /api/vehicles/{id} | ✓ | ✗ |
| GET /api/vehicles/{id} | ✓ | ✓ |
| GET /api/parts | ✓ | ✓ |
| POST /api/parts | ✓ | ✗ |
| PUT /api/parts/{id} | ✓ | ✗ |
| DELETE /api/parts/{id} | ✓ | ✗ |
| GET /api/parts/{id} | ✓ | ✓ |
| GET /api/relations | ✓ | ✓ |
| POST /api/relations | ✓ | ✗ |
| PUT /api/relations/{id} | ✓ | ✗ |
| DELETE /api/relations/{id} | ✓ | ✗ |
| GET /api/vehicles/{vid}/parts | ✓ | ✓ |
| GET /api/parts/{pid}/vehicles | ✓ | ✓ |
| GET /api/dashboard/statistics | ✓ | ✓ |

---

## 三、后端项目目录结构

```
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
│   ├── main.py                      # FastAPI 应用入口
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # 配置管理（环境变量、数据库连接）
│   │   ├── security.py              # JWT 生成/验证、密码加密
│   │   ├── deps.py                  # FastAPI 依赖注入（当前用户、数据库会话）
│   │   └── exceptions.py            # 自定义异常处理
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                  # SQLAlchemy 基类
│   │   ├── user.py                  # SysUser 模型
│   │   ├── role.py                  # SysRole 模型
│   │   ├── vehicle.py               # VehicleInfo 模型
│   │   ├── part.py                  # PartInfo 模型
│   │   └── vehicle_part.py          # VehiclePartRelation 模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py                # 统一响应模型（Result、PageResponse）
│   │   ├── auth.py                  # 认证相关 Schema
│   │   ├── user.py                  # 用户 Schema
│   │   ├── role.py                  # 角色 Schema
│   │   ├── vehicle.py               # 整车 Schema
│   │   ├── part.py                  # 零部件 Schema
│   │   └── vehicle_part.py          # 装配关系 Schema
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py                  # 泛型 CRUD 基类
│   │   ├── user.py                  # 用户 CRUD
│   │   ├── role.py                  # 角色 CRUD
│   │   ├── vehicle.py               # 整车 CRUD
│   │   ├── part.py                  # 零部件 CRUD
│   │   └── vehicle_part.py          # 装配关系 CRUD
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py          # 认证业务逻辑
│   │   ├── user_service.py          # 用户业务逻辑
│   │   └── dashboard_service.py     # 首页统计业务逻辑
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py                # 路由注册
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py              # 认证路由
│   │       ├── users.py             # 用户管理路由
│   │       ├── roles.py             # 角色路由
│   │       ├── vehicles.py          # 整车路由
│   │       ├── parts.py             # 零部件路由
│   │       ├── vehicle_parts.py     # 装配关系路由
│   │       └── dashboard.py         # 首页统计路由
│   ├── utils/
│   │   ├── __init__.py
│   │   └── response.py              # 统一响应封装
│   └── config/
│       ├── __init__.py
│       └── settings.py              # Settings 配置类
└── tests/
    ├── __init__.py
    ├── conftest.py                  # Pytest fixture
    ├── test_auth.py
    ├── test_users.py
    ├── test_vehicles.py
    ├── test_parts.py
    └── test_vehicle_parts.py
```

### 3.1 关键文件内容约定

#### app/main.py
- 创建 FastAPI 实例
- 注册 CORS 中间件
- 注册路由前缀 `/api`
- 注册异常处理器
- 挂载 Swagger/OpenAPI

#### app/core/security.py
- `create_access_token(data, expires_delta)` → JWT token
- `verify_token(token)` → 解析 payload
- `get_password_hash(password)` → bcrypt 哈希
- `verify_password(plain, hashed)` → 验证密码

#### app/core/deps.py
- `get_db()` → 数据库 session 依赖
- `get_current_user()` → 从 Header 提取 Token 并验证，返回当前用户
- `require_admin()` → 检查当前用户角色是否为 admin

#### app/crud/base.py
- 泛型基类：`create()`, `get_by_id()`, `get_multi()`, `update()`, `remove()`, `get_multi_filtered()`（支持条件搜索+分页）

#### app/utils/response.py
- `success_response(data, message)` → 统一成功响应
- `error_response(code, message)` → 统一错误响应
- `page_response(items, total, page, page_size)` → 分页响应

#### app/schemas/common.py
```python
class Result(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None

class PageResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
```

---

## 四、前端项目目录结构

```
frontend/
├── README.md
├── package.json
├── vite.config.js
├── index.html
├── .env.development
├── .env.production
├── public/
│   └── favicon.ico
├── src/
│   ├── main.jsx                       # React 入口
│   ├── App.jsx                        # 根组件（路由配置）
│   ├── assets/
│   │   ├── images/
│   │   └── styles/
│   │       └── global.css             # 全局样式
│   ├── api/
│   │   ├── request.js                 # Axios 封装（拦截器、token、统一错误）
│   │   ├── auth.js                    # 认证 API
│   │   ├── user.js                    # 用户 API
│   │   ├── role.js                    # 角色 API
│   │   ├── vehicle.js                 # 整车 API
│   │   ├── part.js                    # 零部件 API
│   │   ├── vehiclePart.js             # 装配关系 API
│   │   └── dashboard.js               # 首页统计 API
│   ├── store/
│   │   ├── index.js                   # Redux store 配置
│   │   ├── slices/
│   │   │   ├── authSlice.js           # 认证状态（token, user, roles）
│   │   │   └── appSlice.js            # 全局状态（侧边栏折叠等）
│   ├── components/
│   │   ├── Layout/
│   │   │   ├── MainLayout.jsx         # 主布局（左侧菜单 + 顶部栏 + 内容区）
│   │   │   └── Header.jsx             # 顶部栏（用户信息、退出）
│   │   ├── SearchForm/
│   │   │   └── index.jsx             # 搜索表单组件
│   │   └── DataTable/
│   │       └── index.jsx             # 分页表格组件
│   ├── pages/
│   │   ├── Login/
│   │   │   └── index.jsx             # 登录页
│   │   ├── Dashboard/
│   │   │   └── index.jsx             # 首页仪表盘
│   │   ├── UserManage/
│   │   │   └── index.jsx             # 用户管理
│   │   ├── RoleManage/
│   │   │   └── index.jsx             # 角色管理
│   │   ├── VehicleManage/
│   │   │   └── index.jsx             # 整车管理
│   │   ├── PartManage/
│   │   │   └── index.jsx             # 零部件管理
│   │   ├── RelationManage/
│   │   │   └── index.jsx             # 装配关系管理
│   │   └── ProfilePassword/
│   │       └── index.jsx             # 修改密码
│   ├── router/
│   │   ├── index.js                   # React Router 配置
│   │   └── routes.js                  # 路由定义 + 权限守卫
│   └── utils/
│       ├── auth.js                    # Token 存取（localStorage）
│       └── constants.js               # 常量（角色名、状态枚举等）
└── package.json
```

### 4.1 关键文件约定

#### src/api/request.js
- 创建 Axios 实例，baseURL 从环境变量读取
- 请求拦截器：自动附加 `Authorization: Bearer <token>`
- 响应拦截器：
  - `code === 200` → 返回 `data`
  - `code === 401` → 清除 Token，跳转登录页
  - 其他错误 → 显示 `message`（antd message.error）

#### src/store/slices/authSlice.js
- State: `{ token: null, user: null, roles: [] }`
- Actions: `login()`, `logout()`, `setUser()`

#### src/router/routes.js
- 公开路由: `/login`
- 受保护路由: 全部其他路由
- 权限守卫: 非 admin 用户访问管理页面时重定向至首页或显示无权限提示

#### src/components/Layout/MainLayout.jsx
- Ant Design Layout: `<Sider>` 左侧菜单 + `<Layout>` 顶部 `<Header>` + `<Content>`
- 菜单项:
  - 首页 (Dashboard)
  - 用户管理 (仅 admin)
  - 角色管理 (仅 admin)
  - 整车管理
  - 零部件管理
  - 装配关系管理

---

## 五、前端页面设计

### 5.1 登录页 (Login)

**布局**: 居中卡片，包含 Logo 标题 + 登录表单
**表单字段**:
- username (Input) - 必填
- password (Password) - 必填
- 登录按钮
**调用接口**: `POST /api/auth/login`
**交互**: 登录成功 → 存储 Token 到 localStorage → 跳转 `/`；失败 → 显示错误消息

### 5.2 首页 (Dashboard)

**布局**: 四列统计卡片 + 两行图表
**内容**:
- 第一行: 4 张统计卡片（整车总数、零部件总数、用户总数、库存预警数）
- 第二行: 左侧零部件类别统计柱状图 + 右侧库存预警统计列表
- 第三行: 左侧最近新增整车列表 (Table) + 右侧最近新增零部件列表 (Table)

**调用接口**: `GET /api/dashboard/statistics`

### 5.3 用户管理 (UserManage)

**查询区域**: 用户名（输入框）、真实姓名（输入框）、搜索按钮、重置按钮
**表格字段**: ID、用户名、真实姓名、手机号、邮箱、角色标签、状态（启用/停用开关）、创建时间、操作
**操作按钮**: 新增用户（admin 可见）、编辑（admin）、删除（admin）、启用/停用（admin）
**Modal 表单字段**: 用户名（新增时必填，编辑时只读）、真实姓名、密码（新增时必填，编辑时可选修改）、手机号、邮箱、角色（多选，从角色接口获取）、状态（开关）
**调用接口**: `GET /api/users`, `POST /api/users`, `PUT /api/users/{id}`, `DELETE /api/users/{id}`, `PUT /api/users/{id}/status`
**按钮权限**: 新增/编辑/删除/停用按钮仅 admin 可见；viewer 只能查看

### 5.4 角色管理 (RoleManage)

**布局**: 静态表格，展示两个固定角色
**表格字段**: ID、角色名称、角色描述
**操作**: 仅查看，不可增删改（角色为系统预设）
**调用接口**: `GET /api/roles`

### 5.5 整车管理 (VehicleManage)

**查询区域**: 整车编号（输入框）、整车名称（输入框）、品牌（输入框）、搜索按钮、重置按钮
**表格字段**: ID、整车编号、整车名称、整车型号、品牌、年款、发动机型号、创建时间、操作
**操作按钮**: 新增（admin）、编辑（admin）、删除（admin）、查看详情
**Modal 表单字段**: 整车编号（新增必填）、整车名称、整车型号、品牌、年款、发动机型号、描述（TextArea）
**调用接口**: `GET /api/vehicles`, `POST /api/vehicles`, `PUT /api/vehicles/{id}`, `DELETE /api/vehicles/{id}`, `GET /api/vehicles/{id}`

### 5.6 零部件管理 (PartManage)

**查询区域**: 零件编号（输入框）、零件名称（输入框）、类别（输入框）、供应商（输入框）、搜索按钮、重置按钮
**表格字段**: ID、零件编号、零件名称、类别、规格型号、供应商、单位、单价、库存数量、安全库存、库存预警标识、创建时间、操作
**库存预警**: 当 `stock_qty < safe_stock` 时，该行显示红色 `⚠ 库存不足` 标签
**操作按钮**: 新增（admin）、编辑（admin）、删除（admin）、查看详情
**Modal 表单字段**: 零件编号（新增必填）、零件名称、类别、规格型号、材质、供应商、单位、单价（InputNumber）、库存数量（InputNumber）、安全库存（InputNumber）、描述（TextArea）
**调用接口**: `GET /api/parts`, `POST /api/parts`, `PUT /api/parts/{id}`, `DELETE /api/parts/{id}`, `GET /api/parts/{id}`

### 5.7 装配关系管理 (RelationManage)

**布局**: 左侧整车选择器 + 右侧关系表格
**查询区域**: 整车选择（Select，支持搜索），选择后加载该整车全部装配关系
**表格字段**: 关联ID、零件编号、零件名称、类别、装配数量、装配位置、备注、操作
**操作按钮**: 新增装配关系（admin）、编辑（admin）、删除（admin）
**新增/编辑 Modal 表单字段**: 零部件选择（Select，从全部零件中选择）、装配数量（InputNumber）、装配位置（Input）、备注（Input）
**BOM 清单**: 选择整车后可查看完整 BOM 列表
**引用查询**: 在零部件详情中可跳转到引用整车列表
**调用接口**: `GET /api/relations`, `POST /api/relations`, `PUT /api/relations/{id}`, `DELETE /api/relations/{id}`, `GET /api/vehicles/{id}/parts`, `GET /api/parts/{id}/vehicles`
**按钮权限**: 所有写操作仅 admin

### 5.8 修改密码 (ProfilePassword)

**布局**: 居中表单
**表单字段**: 旧密码、新密码、确认新密码
**调用接口**: `PUT /api/auth/change-password`

---

## 六、AI 代码生成实施说明

### 6.1 代码生成顺序

按以下顺序生成代码，每一步完成后可独立验证：

**第一阶段：后端基础**
1. 项目骨架搭建（目录结构、requirements.txt、.env.example）
2. 数据库配置 + SQLAlchemy 模型
3. Alembic 迁移文件
4. 统一响应封装 + 异常处理
5. JWT 认证 + 密码加密

**第二阶段：后端业务**
6. CRUD 基类 + 各实体 CRUD
7. 认证接口（login/userinfo/change-password）
8. 用户管理接口 + 角色接口
9. 整车 + 零部件 CRUD 接口
10. 装配关系接口
11. 首页统计接口

**第三阶段：前端基础**
12. 项目骨架（Vite + React + Ant Design）
13. Axios 封装 + Token 管理 + 路由守卫
14. 主布局（侧边栏菜单 + 顶栏）
15. 登录页 + 首页

**第四阶段：前端业务**
16. 用户管理页 + 角色管理页
17. 整车管理页
18. 零部件管理页
19. 装配关系管理页
20. 修改密码页

### 6.2 字段一致性规则

| 规则 | 说明 |
|------|------|
| 后端 Model 字段名 = API 字段名 = 前端表单字段名 | 三者必须完全一致（snake_case） |
| 前端表单字段类型与后端 Pydantic Schema 类型一致 | 字符串对应 Input，数字对应 InputNumber，日期对应 DatePicker |
| 新增/编辑共用同一 Modal | 通过 `isEdit` 标志区分，编辑时回填数据 |
| 所有列表页支持分页 | 前端使用 `pagination` 属性，后端接收 `page`/`page_size` |
| 所有搜索支持重置 | 重置按钮清空所有搜索字段 |

### 6.3 统一 Result 封装

后端所有接口返回必须通过 `utils/response.py` 中的封装：

```python
# 成功响应
def success_response(data=None, message="success"):
    return {"code": 200, "message": message, "data": data}

# 错误响应
def error_response(code=400, message="error"):
    return {"code": code, "message": message, "data": None}

# 分页响应
def page_response(items, total, page=1, page_size=10):
    return {"items": items, "total": total, "page": page, "page_size": page_size}
```

### 6.4 前端 Token 管理

```javascript
// src/utils/auth.js
export const getToken = () => localStorage.getItem('token')
export const setToken = (token) => localStorage.setItem('token', token)
export const removeToken = () => localStorage.removeItem('token')
export const getUser = () => JSON.parse(localStorage.getItem('user') || 'null')
export const setUser = (user) => localStorage.setItem('user', JSON.stringify(user))
export const clearUser = () => { localStorage.removeItem('user'); localStorage.removeItem('token') }
```

### 6.5 环境变量配置

**后端 .env**:
```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/vehicle_parts?charset=utf8mb4
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

**前端 .env.development**:
```
VITE_API_BASE_URL=http://localhost:8000
```

**前端 .env.production**:
```
VITE_API_BASE_URL=/api
```

---

## 七、开发注意事项

### 7.1 数据库实体字段命名
- 所有数据库模型字段使用 `snake_case`
- SQLAlchemy Column 名必须与 API 返回的 JSON key 一致
- Pydantic Schema 的 `model_config = ConfigDict(from_attributes=True)` 必须设置

### 7.2 前后端字段映射
- 前端表单使用 `Form.Item` 的 `name` 属性绑定后端字段名（snake_case）
- Ant Design `Table` 的 `columns` 中 `dataIndex` 必须与后端返回字段名一致
- `low_stock` 是后端计算字段，用于前端预警标记

### 7.3 CRUD 页面规范
- 每个管理页面必须包含：搜索区域 + 操作按钮区 + 数据表格 + 分页
- 新增/编辑共用 Modal 弹窗，通过 `open` 状态控制显示
- 删除操作必须使用 `Popconfirm` 确认
- 所有异步操作显示 `loading` 状态

### 7.4 错误处理
- 后端：使用 FastAPI `HTTPException` + 自定义异常处理器，返回统一 Result 格式
- 前端：Axios 响应拦截器统一处理错误，`message.error()` 显示提示
- 表单验证：后端 Pydantic 验证 + 前端 Ant Design Form rules 双重校验

### 7.5 性能要求（来自宪法）
- UI 响应时间 ≤ 100ms
- API P95 延迟 ≤ 200ms
- 列表页支持分页，避免一次性加载全部数据
- 首页统计接口使用聚合查询，避免 N+1
