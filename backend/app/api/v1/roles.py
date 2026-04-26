from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.base import get_async_session
from app.models.role import SysRole
from app.core.deps import get_current_user
from app.utils.response import success_response

router = APIRouter()


@router.get("", response_model=dict)
async def list_roles(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(SysRole).order_by(SysRole.id))
    roles = list(result.scalars().all())
    data = [{"id": r.id, "role_name": r.role_name, "role_desc": r.role_desc, "create_time": r.create_time} for r in roles]
    return success_response(data=data)
