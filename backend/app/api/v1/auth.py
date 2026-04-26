from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.base import get_async_session
from app.models.user import SysUser
from app.models.user_role import SysUserRole
from app.models.role import SysRole
from app.schemas.auth import LoginRequest, ChangePasswordRequest, TokenResponse, UserResponse
from app.schemas.user import UserUpdate
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.deps import get_current_user
from app.utils.response import success_response, error_response

router = APIRouter()


@router.post("/login", response_model=dict)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(
        select(SysUser).where(SysUser.username == body.username, SysUser.is_deleted == 0)
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.password):
        return success_response(data=None, message="用户名或密码错误")
    if user.status == 0:
        return success_response(data=None, message="用户已被停用")
    # Get roles
    role_result = await db.execute(
        select(SysRole.role_name)
        .join(SysUserRole, SysUserRole.role_id == SysRole.id)
        .where(SysUserRole.user_id == user.id)
    )
    roles = [r[0] for r in role_result.all()]
    token = create_access_token(data={"sub": str(user.id)})
    return success_response(data={"token": token, "token_type": "Bearer"})


@router.get("/userinfo", response_model=dict)
async def get_userinfo(current_user: SysUser = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)):
    role_result = await db.execute(
        select(SysRole.role_name)
        .join(SysUserRole, SysUserRole.role_id == SysRole.id)
        .where(SysUserRole.user_id == current_user.id)
    )
    roles = [r[0] for r in role_result.all()]
    return success_response(data={
        "id": current_user.id,
        "username": current_user.username,
        "real_name": current_user.real_name,
        "phone": current_user.phone,
        "email": current_user.email,
        "roles": roles,
        "status": current_user.status,
        "create_time": current_user.create_time,
        "update_time": current_user.update_time,
    })


@router.put("/change-password", response_model=dict)
async def change_password(
    body: ChangePasswordRequest,
    db: AsyncSession = Depends(get_async_session),
    current_user: SysUser = Depends(get_current_user),
):
    if not verify_password(body.old_password, current_user.password):
        return success_response(data=None, message="旧密码不正确")
    if len(body.new_password) < 6:
        return success_response(data=None, message="新密码长度不能少于6位")
    current_user.password = get_password_hash(body.new_password)
    await db.commit()
    return success_response(data=None, message="密码修改成功")
