from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.roles import router as roles_router
from app.api.v1.vehicles import router as vehicles_router
from app.api.v1.parts import router as parts_router
from app.api.v1.vehicle_parts import router as vehicle_parts_router
from app.api.v1.dashboard import router as dashboard_router


def include_routers(app: FastAPI):
    app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
    app.include_router(users_router, prefix="/api/users", tags=["用户管理"])
    app.include_router(roles_router, prefix="/api/roles", tags=["角色"])
    app.include_router(vehicles_router, prefix="/api/vehicles", tags=["整车"])
    app.include_router(parts_router, prefix="/api/parts", tags=["零部件"])
    app.include_router(vehicle_parts_router, prefix="/api", tags=["装配关系"])
    app.include_router(dashboard_router, prefix="/api/dashboard", tags=["首页统计"])
