# Tasks: 整车零部件管理系统（Vehicle Parts Management System）

**Input**: Design documents from `specs/002-vehicle-parts-mgmt/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, research.md, quickstart.md, contracts/

**Tests**: Tests are MANDATORY per the project constitution (TDD-driven, ≥ 90% coverage). Every feature task must have corresponding test tasks.

**Organization**: Tasks are organized by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/`, `backend/tests/`
- **Frontend**: `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure per plan.md
- [x] T002 [P] Create backend/app/__init__.py and all subpackage __init__.py files
- [x] T003 [P] Create backend/requirements.txt with all dependencies (fastapi, sqlalchemy, pydantic, pymysql, bcrypt, python-jose, alembic, loguru, uvicorn, pytest, pytest-cov, httpx, pytest-asyncio)
- [x] T004 [P] Create backend/.env.example with DATABASE_URL, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
- [x] T005 Create backend/alembic.ini configured to read sqlalchemy.url from environment
- [x] T006 [P] Create frontend directory structure per plan.md
- [x] T007 [P] Create frontend/package.json with dependencies (react, react-dom, react-router-dom, @reduxjs/toolkit, react-redux, antd, axios, echarts, echarts-for-react, vite)
- [x] T008 [P] Create frontend/vite.config.js with /api proxy to backend
- [x] T009 [P] Create frontend/.env.development (VITE_API_BASE_URL=http://localhost:8000) and .env.production (VITE_API_BASE_URL=/api)
- [x] T010 [P] Create frontend/index.html entry point

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can begin

- [x] T011 Implement backend/app/config/settings.py with pydantic-settings BaseSettings reading from .env
- [x] T012 Implement backend/app/core/config.py with database URL, secret key, token config constants
- [x] T013 [P] Implement backend/app/models/base.py with SQLAlchemy declarative_base and async session factory
- [x] T014 [P] Implement backend/app/utils/response.py with success_response(), error_response(), page_response()
- [x] T015 [P] Implement backend/app/schemas/common.py with Result and PageResponse Pydantic models
- [x] T016 Implement backend/app/core/security.py with create_access_token(), verify_token(), get_password_hash(), verify_password()
- [x] T017 Implement backend/app/core/deps.py with get_db() (AsyncSession), get_current_user() (JWT validation), require_admin() (role check)
- [x] T018 Implement backend/app/core/exceptions.py with custom NotFoundException, DuplicateException, ForbiddenException
- [x] T019 Implement backend/app/main.py with FastAPI app, CORS middleware, /api prefix router registration, exception handlers, Swagger docs
- [x] T020 Create alembic/env.py with async engine support and auto-discover models
- [x] T021 Create alembic/versions/001_initial_schema.py with all 6 table definitions matching tech-spec.md SQL
- [x] T022 Create backend/scripts/seed_data.py to insert admin/viewer roles and initial admin user (username: admin, password: admin123)
- [x] T023 [P] Implement frontend/src/utils/auth.js with getToken, setToken, removeToken, getUser, setUser, clearUser (localStorage)
- [x] T024 [P] Implement frontend/src/utils/constants.js with ROLE_ADMIN, ROLE_VIEWER, status enums
- [x] T025 [P] Implement frontend/src/api/request.js with Axios instance, request interceptor (Bearer token), response interceptor (401 → redirect login, error message)
- [x] T026 Implement frontend/src/store/slices/authSlice.js with login/logout/setUser actions, token/user/roles state
- [x] T027 Implement frontend/src/store/index.js with configureStore combining authSlice
- [ ] T028 Implement frontend/src/assets/styles/global.css with base styles
- [ ] T029 [P] Implement frontend/src/components/Layout/Header.jsx with user info display and logout button
- [x] T030 Implement frontend/src/components/Layout/MainLayout.jsx with Ant Design Sider menu (Dashboard, UserManage, RoleManage, VehicleManage, PartManage, RelationManage) and admin-only menu filtering

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - 管理员登录与首页概览（Priority: P1） 🎯 MVP

**Goal**: 用户可登录系统，查看首页统计数据和图表

**Independent Test**: 使用 admin/admin123 登录成功，跳转首页，看到统计卡片和图表数据

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (Red-Green-Refactor)**

- [ ] T031 [P] [US1] Test POST /api/auth/login success in backend/tests/test_auth.py
- [ ] T032 [P] [US1] Test POST /api/auth/login failure (wrong password) in backend/tests/test_auth.py
- [ ] T033 [P] [US1] Test GET /api/auth/userinfo with valid token in backend/tests/test_auth.py
- [ ] T034 [P] [US1] Test PUT /api/auth/change-password in backend/tests/test_auth.py
- [ ] T035 [US1] Test GET /api/dashboard/statistics returns correct counts in backend/tests/test_auth.py

### Implementation for User Story 1

- [x] T036 [P] [US1] Create SysUser model in backend/app/models/user.py
- [x] T037 [P] [US1] Create SysRole model in backend/app/models/role.py
- [x] T038 [P] [US1] Create SysUserRole model in backend/app/models/user.py
- [x] T039 [US1] Create auth schemas in backend/app/schemas/auth.py (LoginRequest, ChangePasswordRequest, TokenResponse, UserResponse)
- [x] T040 [US1] Create user schemas in backend/app/schemas/user.py (UserCreate, UserUpdate, UserResponse)
- [x] T041 [US1] Create role schemas in backend/app/schemas/role.py (RoleResponse)
- [x] T042 [US1] Implement base CRUD in backend/app/crud/base.py (generic create, get_by_id, get_multi, update, remove, get_multi_filtered)
- [x] T043 [US1] Implement user CRUD in backend/app/crud/user.py (with soft delete, unique username check)
- [x] T044 [US1] Implement role CRUD in backend/app/crud/role.py
- [x] T045 [US1] Implement auth_service.py with login logic (verify password, check status, generate JWT, return token)
- [x] T046 [US1] Implement auth routes in backend/app/api/v1/auth.py (POST /login, GET /userinfo, PUT /change-password)
- [x] T047 [US1] Implement user_service.py with business logic
- [x] T048 [US1] Implement dashboard_service.py with aggregate queries (COUNT vehicles, parts, users, low_stock parts, category stats, recent lists)
- [x] T049 [US1] Implement dashboard routes in backend/app/api/v1/dashboard.py (GET /statistics)
- [x] T050 [US1] Register all v1 routes in backend/app/api/v1/__init__.py and backend/app/api/router.py
- [x] T051 [US1] Create frontend/src/pages/Login/index.jsx with centered card form (username, password), login button, error display
- [x] T052 [US1] Create frontend/src/api/auth.js (loginApi, getUserInfoApi, changePasswordApi)
- [x] T053 [US1] Create frontend/src/api/dashboard.js (getStatisticsApi)
- [x] T054 [US1] Create frontend/src/pages/Dashboard/index.jsx with 4 stat cards, ECharts category bar chart, low stock table, recent vehicles table, recent parts table
- [x] T055 [US1] Implement frontend/src/router/routes.jsx with /login (public), / (protected with MainLayout), auth guard redirect logic
- [x] T056 [US1] Implement frontend/src/App.jsx with RouterProvider, Redux Provider, Ant Design ConfigProvider
- [x] T057 [US1] Implement frontend/src/main.jsx entry point

**Checkpoint**: Login works, dashboard shows statistics. Independent test: login → see stats → logout

---

## Phase 4: User Story 2 - 用户管理（Priority: P1）

**Goal**: 超级管理员可新增、编辑、删除用户，分配角色，启用/停用

**Independent Test**: admin 新增用户 zhangsan，编辑信息，分配 viewer 角色，在列表中可见，停用后无法登录

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (Red-Green-Refactor)**

- [ ] T058 [P] [US2] Test GET /api/users pagination and filtering in backend/tests/test_users.py
- [ ] T059 [P] [US2] Test POST /api/users creates user with roles in backend/tests/test_users.py
- [ ] T060 [P] [US2] Test PUT /api/users/{id} updates user in backend/tests/test_users.py
- [ ] T061 [P] [US2] Test DELETE /api/users/{id} soft deletes in backend/tests/test_users.py
- [ ] T062 [P] [US2] Test PUT /api/users/{id}/status toggles in backend/tests/test_users.py
- [ ] T063 [US2] Test viewer cannot access /api/users (403) in backend/tests/test_users.py

### Implementation for User Story 2

- [x] T064 [P] [US2] Implement user routes in backend/app/api/v1/users.py (GET, POST, PUT, DELETE, PUT /status)
- [x] T065 [P] [US2] Implement role routes in backend/app/api/v1/roles.py (GET /roles)
- [x] T066 [US2] Add admin-only permission check to user/role routes using require_admin() dependency
- [x] T067 [US2] Create frontend/src/api/user.js (getUsersApi, createUserApi, updateUserApi, deleteUserApi, updateUserStatusApi)
- [x] T068 [US2] Create frontend/src/api/role.js (getRolesApi)
- [x] T069 [US2] Create frontend/src/components/SearchForm/index.jsx reusable search form component
- [x] T070 [US2] Create frontend/src/components/DataTable/index.jsx reusable paginated table component
- [x] T071 [US2] Create frontend/src/pages/UserManage/index.jsx with search area (username, real_name), paginated table, action buttons (add/edit/delete/status), role tags, Modal form (username, real_name, password, phone, email, role_ids, status)
- [x] T072 [US2] Create frontend/src/pages/RoleManage/index.jsx with static table showing admin/viewer roles
- [x] T073 [US2] Add admin-only button visibility logic to UserManage (hide add/edit/delete for viewer)

**Checkpoint**: User management fully functional. Independent test: CRUD + role assignment + status toggle

---

## Phase 5: User Story 3 - 整车信息管理（Priority: P2）

**Goal**: 管理员可维护整车数据，支持分页查询和条件搜索

**Independent Test**: 新增整车 VH-001，搜索 brand=Tesla，编辑名称，查看详情，删除

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (Red-Green-Refactor)**

- [ ] T074 [P] [US3] Test GET /api/vehicles pagination and filtering in backend/tests/test_vehicles.py
- [ ] T075 [P] [US3] Test POST /api/vehicles creates with unique vehicle_code in backend/tests/test_vehicles.py
- [ ] T076 [P] [US3] Test PUT /api/vehicles/{id} updates in backend/tests/test_vehicles.py
- [ ] T077 [P] [US3] Test DELETE /api/vehicles/{id} soft deletes in backend/tests/test_vehicles.py
- [ ] T078 [P] [US3] Test GET /api/vehicles/{id} returns detail in backend/tests/test_vehicles.py

### Implementation for User Story 3

- [x] T079 [P] [US3] Create VehicleInfo model in backend/app/models/vehicle.py
- [x] T080 [P] [US3] Create vehicle schemas in backend/app/schemas/vehicle.py (VehicleCreate, VehicleUpdate, VehicleResponse)
- [x] T081 [US3] Implement vehicle CRUD in backend/app/crud/vehicle.py (with soft delete, unique vehicle_code check)
- [x] T082 [US3] Implement vehicle routes in backend/app/api/v1/vehicles.py (GET list, POST, PUT, DELETE, GET detail)
- [x] T083 [US3] Create frontend/src/api/vehicle.js (getVehiclesApi, createVehicleApi, updateVehicleApi, deleteVehicleApi, getVehicleDetailApi)
- [x] T084 [US3] Create frontend/src/pages/VehicleManage/index.jsx with search (vehicle_code, vehicle_name, brand), paginated table, Modal form (vehicle_code, vehicle_name, vehicle_model, brand, year_model, engine_model, description), detail modal, admin-only write buttons

**Checkpoint**: Vehicle management fully functional. Independent test: CRUD + search + pagination

---

## Phase 6: User Story 4 - 零部件信息管理（Priority: P2）

**Goal**: 管理员可维护零部件数据，支持搜索，库存预警标记

**Independent Test**: 新增零件 stock_qty=80, safe_stock=100，列表中显示预警标记，搜索 category=制动系统

### Tests for User Story 4

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (Red-Green-Refactor)**

- [ ] T085 [P] [US4] Test GET /api/parts pagination, filtering, low_stock calculation in backend/tests/test_parts.py
- [ ] T086 [P] [US4] Test POST /api/parts creates with unique part_code in backend/tests/test_parts.py
- [ ] T087 [P] [US4] Test PUT /api/parts/{id} updates in backend/tests/test_parts.py
- [ ] T088 [P] [US4] Test DELETE /api/parts/{id} soft deletes in backend/tests/test_parts.py
- [ ] T089 [P] [US4] Test GET /api/parts/{id} returns detail in backend/tests/test_parts.py

### Implementation for User Story 4

- [x] T090 [P] [US4] Create PartInfo model in backend/app/models/part.py
- [x] T091 [P] [US4] Create part schemas in backend/app/schemas/part.py (PartCreate, PartUpdate, PartResponse with low_stock computed field)
- [x] T092 [US4] Implement part CRUD in backend/app/crud/part.py (with soft delete, unique part_code check, low_stock calculation)
- [x] T093 [US4] Implement part routes in backend/app/api/v1/parts.py (GET list, POST, PUT, DELETE, GET detail)
- [x] T094 [US4] Create frontend/src/api/part.js (getPartsApi, createPartApi, updatePartApi, deletePartApi, getPartDetailApi)
- [x] T095 [US4] Create frontend/src/pages/PartManage/index.jsx with search (part_code, part_name, category, supplier), paginated table with low_stock warning badge, Modal form (part_code, part_name, category, spec_model, material, supplier, unit, price, stock_qty, safe_stock, description), admin-only write buttons

**Checkpoint**: Part management fully functional. Independent test: CRUD + search + low_stock badge

---

## Phase 7: User Story 5 - 整车零部件装配关系管理（Priority: P2）

**Goal**: 管理员可为整车配置零部件装配关系，查看 BOM 清单和引用

**Independent Test**: 选择整车 VH-001，添加零件 PRT-001 数量=2 位置=左前轮，查看 BOM 清单包含该零件

### Tests for User Story 5

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (Red-Green-Refactor)**

- [ ] T096 [P] [US5] Test GET /api/relations pagination in backend/tests/test_vehicle_parts.py
- [ ] T097 [P] [US5] Test POST /api/relations creates with unique (vehicle_id, part_id) in backend/tests/test_vehicle_parts.py
- [ ] T098 [P] [US5] Test PUT /api/relations/{id} updates in backend/tests/test_vehicle_parts.py
- [ ] T099 [P] [US5] Test DELETE /api/relations/{id} deletes in backend/tests/test_vehicle_parts.py
- [ ] T100 [P] [US5] Test GET /api/vehicles/{id}/parts returns BOM in backend/tests/test_vehicle_parts.py
- [ ] T101 [P] [US5] Test GET /api/parts/{id}/vehicles returns referencing vehicles in backend/tests/test_vehicle_parts.py

### Implementation for User Story 5

- [x] T102 [P] [US5] Create VehiclePartRelation model in backend/app/models/vehicle_part.py
- [x] T103 [P] [US5] Create vehicle_part schemas in backend/app/schemas/vehicle_part.py (RelationCreate, RelationUpdate, RelationResponse, BOMResponse)
- [x] T104 [US5] Implement relation CRUD in backend/app/crud/vehicle_part.py (with unique vehicle_id+part_id check)
- [x] T105 [US5] Implement relation routes in backend/app/api/v1/vehicle_parts.py (GET relations, POST, PUT, DELETE, GET /vehicles/{id}/parts, GET /parts/{id}/vehicles)
- [x] T106 [US5] Create frontend/src/api/vehiclePart.js (getRelationsApi, createRelationApi, updateRelationApi, deleteRelationApi, getVehicleBomApi, getPartVehiclesApi)
- [x] T107 [US5] Create frontend/src/pages/RelationManage/index.jsx with vehicle selector (Select with search), relation table (part_code, part_name, category, quantity, position, remark), Modal form (part_id select, quantity, position_name, remark), admin-only write buttons, BOM detail view

**Checkpoint**: Relation management fully functional. Independent test: add/edit/delete relations, view BOM

---

## Phase 8: User Story 6 - 统计分析（Priority: P3）

**Goal**: 首页展示统计卡片和可视化图表

**Independent Test**: 首页数据与数据库记录一致，类别柱状图正确，预警列表准确，最近新增显示最新 10 条

### Tests for User Story 6

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (Red-Green-Refactor)**

- [ ] T108 [P] [US6] Test dashboard statistics accuracy with seeded data in backend/tests/test_auth.py (add to existing file)

### Implementation for User Story 6

- [x] T109 [US6] Enhance dashboard_service.py to compute category_stats (GROUP BY category), low_stock_parts list, recent_vehicles (ORDER BY create_time DESC LIMIT 10), recent_parts (ORDER BY create_time DESC LIMIT 10)
- [x] T110 [US6] Enhance Dashboard page ECharts integration with category bar chart data binding
- [x] T111 [US6] Add low_stock_parts table to Dashboard with part_code, part_name, stock_qty, safe_stock columns
- [x] T112 [US6] Add recent_vehicles and recent_parts tables to Dashboard with create_time sorting

**Checkpoint**: Dashboard shows all statistics accurately. Independent test: verify counts match DB

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T113 [P] Add pytest configuration (pytest.ini, conftest.py with db fixture, test client, admin/viewer auth fixtures)
- [ ] T114 [P] Add ESLint + Prettier configuration to frontend
- [ ] T115 Run coverage report on backend tests, verify ≥ 90% line and branch coverage
- [x] T116 Add loading states to all frontend async operations (Spin, button loading)
- [x] T117 Add Popconfirm to all delete operations across all pages
- [ ] T118 Add error boundary and 404 page to frontend router
- [ ] T119 [P] Create backend/README.md with setup and run instructions
- [ ] T120 [P] Create frontend/README.md with setup and run instructions
- [ ] T121 Verify quickstart.md steps work end-to-end (fresh clone → running app)
- [ ] T122 Run performance check: list pages load ≤ 2s with 500 records, API P95 ≤ 200ms

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) or sequentially in priority order
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: After Foundational - No dependencies on other stories → **MVP**
- **User Story 2 (P1)**: After Foundational - Depends on US1 auth infrastructure for permission checks
- **User Story 3 (P2)**: After Foundational - No dependencies on other stories
- **User Story 4 (P2)**: After Foundational - No dependencies on other stories
- **User Story 5 (P2)**: After Foundational - Depends on US3 (vehicles) and US4 (parts) entities existing
- **User Story 6 (P3)**: After Foundational - Dashboard service depends on all entities for aggregate queries

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Backend before frontend pages that consume the APIs
- Core implementation before integration

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, US3 and US4 can start in parallel (they are independent)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel

---

## Parallel Example: User Story 3

```bash
# Launch all tests for User Story 3 together:
Task: "Test GET /api/vehicles pagination" [T074]
Task: "Test POST /api/vehicles creates" [T075]
Task: "Test PUT /api/vehicles/{id}" [T076]
Task: "Test DELETE /api/vehicles/{id}" [T077]
Task: "Test GET /api/vehicles/{id}" [T078]

# Launch all models/schemas for User Story 3 together:
Task: "Create VehicleInfo model" [T079]
Task: "Create vehicle schemas" [T080]
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Login + Dashboard)
4. **STOP and VALIDATE**: Login with admin/admin123, see dashboard stats
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Login + Dashboard) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (User Management) → Test independently → Deploy/Demo
4. Add User Story 3 (Vehicle Management) → Test independently → Deploy/Demo
5. Add User Story 4 (Part Management) → Test independently → Deploy/Demo
6. Add User Story 5 (Relation Management) → Test independently → Deploy/Demo
7. Add User Story 6 (Dashboard Charts) → Test independently → Deploy/Demo
8. Polish phase → Full delivery

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Auth + Dashboard)
   - Developer B: User Story 3 (Vehicles) + User Story 5 (Relations)
   - Developer C: User Story 4 (Parts) + User Story 2 (Users)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
