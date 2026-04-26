# API Contracts: 整车零部件管理系统

> 定义所有 RESTful 接口的请求/响应契约。与 tech-spec.md 第二部分保持一致。

## 统一响应格式

所有接口返回:
```json
{
  "code": 200,
  "message": "success",
  "data": null
}
```

分页列表 data:
```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 10
}
```

错误响应:
```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

## Endpoint Contracts

### POST /api/auth/login
- **Request**: `{ username: string, password: string }`
- **Response 200**: `{ token: string, token_type: string }`
- **Response 401**: `code: 401, message: "用户名或密码错误"`

### GET /api/auth/userinfo
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: `{ id, username, real_name, phone, email, roles: string[], status, create_time }`
- **Response 401**: Token 无效或过期

### PUT /api/auth/change-password
- **Headers**: `Authorization: Bearer <token>`
- **Request**: `{ old_password: string, new_password: string }`
- **Response 200**: `message: "密码修改成功"`
- **Response 400**: 旧密码不正确 或 新密码长度不足

### GET /api/users
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Query**: `page?: number, page_size?: number, username?: string, real_name?: string`
- **Response 200**: PageResponse\<User\>
- **Response 403**: 非 admin 角色

### POST /api/users
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Request**: `{ username, real_name, password, phone?, email?, role_ids: number[] }`
- **Response 200**: User
- **Response 409**: username 已存在

### PUT /api/users/{id}
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Request**: `{ real_name?, phone?, email?, role_ids?, status? }`
- **Response 200**: User
- **Response 404**: 用户不存在

### DELETE /api/users/{id}
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Response 200**: `{ message: "删除成功" }`
- **Response 404**: 用户不存在

### PUT /api/users/{id}/status
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Request**: `{ status: 0 | 1 }`
- **Response 200**: User

### GET /api/roles
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Response 200**: `Role[]`

### GET /api/vehicles
- **Headers**: `Authorization: Bearer <token>`
- **Query**: `page?: number, page_size?: number, vehicle_code?: string, vehicle_name?: string, brand?: string`
- **Response 200**: PageResponse\<Vehicle\>

### POST /api/vehicles
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Request**: `{ vehicle_code, vehicle_name, vehicle_model?, brand?, year_model?, engine_model?, description? }`
- **Response 200**: Vehicle
- **Response 409**: vehicle_code 已存在

### PUT /api/vehicles/{id}
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Request**: Vehicle (partial)
- **Response 200**: Vehicle

### DELETE /api/vehicles/{id}
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Response 200**: `{ message: "删除成功" }`

### GET /api/vehicles/{id}
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: Vehicle

### GET /api/parts
- **Headers**: `Authorization: Bearer <token>`
- **Query**: `page?: number, page_size?: number, part_code?: string, part_name?: string, category?: string, supplier?: string`
- **Response 200**: PageResponse\<Part + low_stock: boolean\>

### POST /api/parts
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Request**: `{ part_code, part_name, category?, spec_model?, material?, supplier?, unit?, price?, stock_qty?, safe_stock?, description? }`
- **Response 200**: Part
- **Response 409**: part_code 已存在

### PUT /api/parts/{id}
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Request**: Part (partial)
- **Response 200**: Part

### DELETE /api/parts/{id}
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Response 200**: `{ message: "删除成功" }`

### GET /api/parts/{id}
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: Part

### GET /api/relations
- **Headers**: `Authorization: Bearer <token>`
- **Query**: `page?: number, page_size?: number, vehicle_id?: number, part_id?: number`
- **Response 200**: PageResponse\<Relation\>

### POST /api/relations
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Request**: `{ vehicle_id, part_id, quantity?, position_name?, remark? }`
- **Response 200**: Relation
- **Response 409**: 该整车+零部件组合已存在

### PUT /api/relations/{id}
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Request**: `{ quantity?, position_name?, remark? }`
- **Response 200**: Relation

### DELETE /api/relations/{id}
- **Headers**: `Authorization: Bearer <token>` (admin only)
- **Response 200**: `{ message: "删除成功" }`

### GET /api/vehicles/{vehicle_id}/parts
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: `{ vehicle: VehicleBrief, parts: RelationDetail[], total_parts: number }`

### GET /api/parts/{part_id}/vehicles
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: `{ part: PartBrief, vehicles: RelationDetail[], total_vehicles: number }`

### GET /api/dashboard/statistics
- **Headers**: `Authorization: Bearer <token>`
- **Response 200**: `{ vehicle_count, part_count, user_count, low_stock_count, category_stats, low_stock_parts, recent_vehicles, recent_parts }`
