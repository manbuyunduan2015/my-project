# Data Model: 整车零部件管理系统

## Entity Definitions

### SysUser (系统用户)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT UNSIGNED | PK, AUTO_INCREMENT | 用户ID |
| username | VARCHAR(64) | UNIQUE, NOT NULL | 用户名（登录用） |
| real_name | VARCHAR(64) | NOT NULL, DEFAULT '' | 真实姓名 |
| password | VARCHAR(128) | NOT NULL | 密码（bcrypt加密） |
| phone | VARCHAR(20) | NOT NULL, DEFAULT '' | 手机号 |
| email | VARCHAR(128) | NOT NULL, DEFAULT '' | 邮箱 |
| status | TINYINT | NOT NULL, DEFAULT 1 | 状态: 1=启用, 0=停用 |
| is_deleted | TINYINT | NOT NULL, DEFAULT 0 | 软删除标志 |
| create_time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| update_time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

**Validation Rules**:
- username: 1-64 字符，全局唯一，不可修改（创建后）
- password: ≥6 字符，存储前 bcrypt 加密
- email: 必须为合法邮箱格式（Pydantic EmailStr）
- phone: 可选，合法手机号格式

### SysRole (系统角色)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT UNSIGNED | PK, AUTO_INCREMENT | 角色ID |
| role_name | VARCHAR(32) | UNIQUE, NOT NULL | 角色名称: admin / viewer |
| role_desc | VARCHAR(128) | NOT NULL, DEFAULT '' | 角色描述 |
| create_time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**Validation Rules**:
- role_name: 仅允许 'admin' 或 'viewer'，系统预设不可增删

### SysUserRole (用户角色关联)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT UNSIGNED | PK, AUTO_INCREMENT | 关联ID |
| user_id | INT UNSIGNED | FK → sys_user.id, NOT NULL | 用户ID |
| role_id | INT UNSIGNED | FK → sys_role.id, NOT NULL | 角色ID |

**Relationships**:
- user_id → SysUser (ON DELETE CASCADE)
- role_id → SysRole (ON DELETE CASCADE)
- UNIQUE(user_id, role_id): 同一用户不能重复分配同一角色

### VehicleInfo (整车信息)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT UNSIGNED | PK, AUTO_INCREMENT | 整车ID |
| vehicle_code | VARCHAR(64) | UNIQUE, NOT NULL | 整车编号 |
| vehicle_name | VARCHAR(128) | NOT NULL | 整车名称 |
| vehicle_model | VARCHAR(128) | NOT NULL, DEFAULT '' | 整车型号 |
| brand | VARCHAR(64) | NOT NULL, DEFAULT '' | 品牌 |
| year_model | VARCHAR(16) | NOT NULL, DEFAULT '' | 年款 |
| engine_model | VARCHAR(128) | NOT NULL, DEFAULT '' | 发动机型号 |
| description | TEXT | NOT NULL, DEFAULT '' | 描述 |
| is_deleted | TINYINT | NOT NULL, DEFAULT 0 | 软删除标志 |
| create_time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| update_time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

**Validation Rules**:
- vehicle_code: 全局唯一
- vehicle_name: 必填，1-128 字符

### PartInfo (零部件信息)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT UNSIGNED | PK, AUTO_INCREMENT | 零部件ID |
| part_code | VARCHAR(64) | UNIQUE, NOT NULL | 零件编号 |
| part_name | VARCHAR(128) | NOT NULL | 零件名称 |
| category | VARCHAR(64) | NOT NULL, DEFAULT '' | 零件类别 |
| spec_model | VARCHAR(128) | NOT NULL, DEFAULT '' | 规格型号 |
| material | VARCHAR(128) | NOT NULL, DEFAULT '' | 材质 |
| supplier | VARCHAR(128) | NOT NULL, DEFAULT '' | 供应商 |
| unit | VARCHAR(16) | NOT NULL, DEFAULT '' | 单位 |
| price | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00 | 单价（元） |
| stock_qty | INT | NOT NULL, DEFAULT 0 | 库存数量 |
| safe_stock | INT | NOT NULL, DEFAULT 0 | 安全库存 |
| description | TEXT | NOT NULL, DEFAULT '' | 描述 |
| is_deleted | TINYINT | NOT NULL, DEFAULT 0 | 软删除标志 |
| create_time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| update_time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE | 更新时间 |

**Validation Rules**:
- part_code: 全局唯一
- price: ≥ 0
- stock_qty: ≥ 0
- safe_stock: ≥ 0
- low_stock: 计算字段，stock_qty < safe_stock 时为 true

### VehiclePartRelation (整车零部件装配关系)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT UNSIGNED | PK, AUTO_INCREMENT | 关联ID |
| vehicle_id | INT UNSIGNED | FK → vehicle_info.id, NOT NULL | 整车ID |
| part_id | INT UNSIGNED | FK → part_info.id, NOT NULL | 零部件ID |
| quantity | INT | NOT NULL, DEFAULT 1 | 装配数量 |
| position_name | VARCHAR(128) | NOT NULL, DEFAULT '' | 装配位置 |
| remark | VARCHAR(256) | NOT NULL, DEFAULT '' | 备注 |
| create_time | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 创建时间 |

**Relationships**:
- vehicle_id → VehicleInfo (ON DELETE CASCADE)
- part_id → PartInfo (ON DELETE CASCADE)
- UNIQUE(vehicle_id, part_id): 同一整车不能重复添加同一零部件

**Validation Rules**:
- quantity: ≥ 1
- vehicle_id: 必须存在且未被软删除
- part_id: 必须存在且未被软删除

## State Transitions

### User Status
```
创建 → status=1 (启用) → [停用] → status=0 (停用) → [启用] → status=1
```
- 停用用户无法登录
- 软删除用户 is_deleted=1，列表不可见

### Soft Delete Pattern
- vehicle_info, part_info, sys_user 使用 is_deleted 标志
- 查询默认过滤 `WHERE is_deleted = 0`
- 删除操作设置 `is_deleted = 1`，不物理删除
