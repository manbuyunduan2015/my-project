from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.models.base import get_async_session
from app.models.part import PartInfo
from app.schemas.part import PartCreate, PartUpdate
from app.core.deps import require_admin, get_current_user
from app.utils.response import success_response, page_response

router = APIRouter()


def _part_to_dict(p):
    return {
        "id": p.id, "part_code": p.part_code, "part_name": p.part_name,
        "category": p.category, "spec_model": p.spec_model, "material": p.material,
        "supplier": p.supplier, "unit": p.unit, "price": float(p.price),
        "stock_qty": p.stock_qty, "safe_stock": p.safe_stock,
        "low_stock": p.stock_qty < p.safe_stock,
        "description": p.description,
        "create_time": p.create_time, "update_time": p.update_time,
    }


@router.get("", response_model=dict)
async def list_parts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=10000),
    part_code: str = Query(""),
    part_name: str = Query(""),
    category: str = Query(""),
    supplier: str = Query(""),
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    filters = [PartInfo.is_deleted == 0]
    if part_code:
        filters.append(PartInfo.part_code.contains(part_code))
    if part_name:
        filters.append(PartInfo.part_name.contains(part_name))
    if category:
        filters.append(PartInfo.category.contains(category))
    if supplier:
        filters.append(PartInfo.supplier.contains(supplier))
    where = and_(*filters)
    offset = (page - 1) * page_size
    total_r = await db.execute(select(func.count()).select_from(PartInfo).where(where))
    total = total_r.scalar() or 0
    stmt = select(PartInfo).where(where).offset(offset).limit(page_size).order_by(PartInfo.id.desc())
    result = await db.execute(stmt)
    items = list(result.scalars().all())
    return success_response(data=page_response([_part_to_dict(p) for p in items], total, page, page_size))


@router.post("", response_model=dict)
async def create_part(
    body: PartCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    existing = await db.execute(select(PartInfo).where(PartInfo.part_code == body.part_code))
    if existing.scalar_one_or_none():
        return success_response(data=None, message="零件编号已存在")
    part = PartInfo(**body.model_dump())
    db.add(part)
    await db.commit()
    await db.refresh(part)
    return success_response(data=_part_to_dict(part))


@router.put("/{part_id}", response_model=dict)
async def update_part(
    part_id: int, body: PartUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    r = await db.execute(select(PartInfo).where(PartInfo.id == part_id, PartInfo.is_deleted == 0))
    part = r.scalar_one_or_none()
    if not part:
        return success_response(data=None, message="零部件不存在")
    update_data = body.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(part, k, v)
    await db.commit()
    await db.refresh(part)
    return success_response(data=_part_to_dict(part))


@router.delete("/{part_id}", response_model=dict)
async def delete_part(
    part_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    r = await db.execute(select(PartInfo).where(PartInfo.id == part_id, PartInfo.is_deleted == 0))
    part = r.scalar_one_or_none()
    if not part:
        return success_response(data=None, message="零部件不存在")
    part.is_deleted = 1
    await db.commit()
    return success_response(data=None, message="删除成功")


@router.get("/{part_id}", response_model=dict)
async def get_part(
    part_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    r = await db.execute(select(PartInfo).where(PartInfo.id == part_id, PartInfo.is_deleted == 0))
    part = r.scalar_one_or_none()
    if not part:
        return success_response(data=None, message="零部件不存在")
    return success_response(data=_part_to_dict(part))
