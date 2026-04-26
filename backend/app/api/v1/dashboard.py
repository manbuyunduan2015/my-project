from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.base import get_async_session
from app.models.vehicle import VehicleInfo
from app.models.part import PartInfo
from app.models.user import SysUser
from app.core.deps import get_current_user
from app.utils.response import success_response

router = APIRouter()


@router.get("/statistics", response_model=dict)
async def get_statistics(
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    # Counts
    v_count = await db.execute(select(func.count(VehicleInfo.id)).where(VehicleInfo.is_deleted == 0))
    vehicle_count = v_count.scalar() or 0
    p_count = await db.execute(select(func.count(PartInfo.id)).where(PartInfo.is_deleted == 0))
    part_count = p_count.scalar() or 0
    u_count = await db.execute(select(func.count(SysUser.id)).where(SysUser.is_deleted == 0))
    user_count = u_count.scalar() or 0

    # Low stock parts
    low_stock_result = await db.execute(
        select(func.count(PartInfo.id)).where(
            PartInfo.is_deleted == 0, PartInfo.stock_qty < PartInfo.safe_stock
        )
    )
    low_stock_count = low_stock_result.scalar() or 0

    # Category stats
    cat_result = await db.execute(
        select(PartInfo.category, func.count(PartInfo.id))
        .where(PartInfo.is_deleted == 0)
        .group_by(PartInfo.category)
    )
    category_stats = [{"category": row[0] or "未分类", "count": row[1]} for row in cat_result.all()]

    # Low stock parts list
    low_parts_result = await db.execute(
        select(PartInfo.part_code, PartInfo.part_name, PartInfo.stock_qty, PartInfo.safe_stock)
        .where(PartInfo.is_deleted == 0, PartInfo.stock_qty < PartInfo.safe_stock)
        .order_by(PartInfo.stock_qty.asc())
        .limit(10)
    )
    low_stock_parts = [
        {"part_code": r[0], "part_name": r[1], "stock_qty": r[2], "safe_stock": r[3]}
        for r in low_parts_result.all()
    ]

    # Recent vehicles
    recent_v_result = await db.execute(
        select(VehicleInfo.id, VehicleInfo.vehicle_code, VehicleInfo.vehicle_name, VehicleInfo.brand, VehicleInfo.create_time)
        .where(VehicleInfo.is_deleted == 0)
        .order_by(VehicleInfo.create_time.desc())
        .limit(10)
    )
    recent_vehicles = [
        {"id": r[0], "vehicle_code": r[1], "vehicle_name": r[2], "brand": r[3], "create_time": r[4]}
        for r in recent_v_result.all()
    ]

    # Recent parts
    recent_p_result = await db.execute(
        select(PartInfo.id, PartInfo.part_code, PartInfo.part_name, PartInfo.category, PartInfo.create_time)
        .where(PartInfo.is_deleted == 0)
        .order_by(PartInfo.create_time.desc())
        .limit(10)
    )
    recent_parts = [
        {"id": r[0], "part_code": r[1], "part_name": r[2], "category": r[3], "create_time": r[4]}
        for r in recent_p_result.all()
    ]

    return success_response(data={
        "vehicle_count": vehicle_count,
        "part_count": part_count,
        "user_count": user_count,
        "low_stock_count": low_stock_count,
        "category_stats": category_stats,
        "low_stock_parts": low_stock_parts,
        "recent_vehicles": recent_vehicles,
        "recent_parts": recent_parts,
    })
