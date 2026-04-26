from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from app.models.base import get_async_session
from app.models.user import SysUser
from app.models.user_role import SysUserRole
from app.models.role import SysRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import get_password_hash
from app.core.deps import require_admin
from app.core.exceptions import NotFoundException, DuplicateException
from app.utils.response import success_response, page_response

router = APIRouter()


async def _get_user_roles(db, user_id):
    result = await db.execute(
        select(SysRole)
        .join(SysUserRole, SysUserRole.role_id == SysRole.id)
        .where(SysUserRole.user_id == user_id)
    )
    return [r[0] for r in result.all()]


async def _assign_roles(db, user_id, role_ids):
    await db.execute(SysUserRole.__table__.delete().where(SysUserRole.user_id == user_id))
    for rid in role_ids:
        db.add(SysUserRole(user_id=user_id, role_id=rid))


def _role_to_dict(role):
    return {"id": role.id, "role_name": role.role_name}


def _to_response(user, roles):
    return {
        "id": user.id, "username": user.username, "real_name": user.real_name,
        "phone": user.phone, "email": user.email,
        "roles": [_role_to_dict(r) for r in roles],
        "status": user.status, "create_time": user.create_time, "update_time": user.update_time,
    }


@router.get("", response_model=dict)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    username: str = Query(""),
    real_name: str = Query(""),
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    filters = [SysUser.is_deleted == 0]
    if username:
        filters.append(SysUser.username.contains(username))
    if real_name:
        filters.append(SysUser.real_name.contains(real_name))
    offset = (page - 1) * page_size
    where = and_(*filters)
    from sqlalchemy import func
    total_r = await db.execute(select(func.count()).select_from(SysUser).where(where))
    total = total_r.scalar() or 0
    stmt = select(SysUser).where(where).offset(offset).limit(page_size).order_by(SysUser.id.desc())
    result = await db.execute(stmt)
    items = list(result.scalars().all())
    data_items = []
    for u in items:
        roles = await _get_user_roles(db, u.id)
        data_items.append(_to_response(u, roles))
    return success_response(data=page_response(data_items, total, page, page_size))


@router.post("", response_model=dict)
async def create_user(
    body: UserCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    existing = await db.execute(select(SysUser).where(SysUser.username == body.username))
    if existing.scalar_one_or_none():
        return success_response(data=None, message="用户名已存在")
    user = SysUser(
        username=body.username, real_name=body.real_name,
        password=get_password_hash(body.password), phone=body.phone, email=body.email,
    )
    db.add(user)
    await db.flush()
    if body.role_ids:
        await _assign_roles(db, user.id, body.role_ids)
    await db.commit()
    await db.refresh(user)
    roles = await _get_user_roles(db, user.id)
    return success_response(data=_to_response(user, roles))


@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: int, body: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    r = await db.execute(select(SysUser).where(SysUser.id == user_id, SysUser.is_deleted == 0))
    user = r.scalar_one_or_none()
    if not user:
        return success_response(data=None, message="用户不存在")
    update_data = body.model_dump(exclude_unset=True)
    role_ids = update_data.pop("role_ids", None)
    for k, v in update_data.items():
        if v is not None:
            setattr(user, k, v)
    if role_ids is not None:
        await _assign_roles(db, user.id, role_ids)
    await db.commit()
    await db.refresh(user)
    roles = await _get_user_roles(db, user.id)
    return success_response(data=_to_response(user, roles))


@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    r = await db.execute(select(SysUser).where(SysUser.id == user_id, SysUser.is_deleted == 0))
    user = r.scalar_one_or_none()
    if not user:
        return success_response(data=None, message="用户不存在")
    user.is_deleted = 1
    await db.commit()
    return success_response(data=None, message="删除成功")


@router.put("/{user_id}/status", response_model=dict)
async def update_user_status(
    user_id: int,
    body: dict,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    r = await db.execute(select(SysUser).where(SysUser.id == user_id, SysUser.is_deleted == 0))
    user = r.scalar_one_or_none()
    if not user:
        return success_response(data=None, message="用户不存在")
    status_val = body.get("status", 1)
    user.status = status_val
    await db.commit()
    await db.refresh(user)
    roles = await _get_user_roles(db, user.id)
    return success_response(data=_to_response(user, roles))
