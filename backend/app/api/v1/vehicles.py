from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.models.base import get_async_session
from app.models.vehicle import VehicleInfo
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.core.deps import require_admin, get_current_user
from app.utils.response import success_response, page_response, error_response

router = APIRouter()


@router.get("", response_model=dict)
async def list_vehicles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=10000),
    vehicle_code: str = Query(""),
    vehicle_name: str = Query(""),
    brand: str = Query(""),
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    filters = [VehicleInfo.is_deleted == 0]
    if vehicle_code:
        filters.append(VehicleInfo.vehicle_code.contains(vehicle_code))
    if vehicle_name:
        filters.append(VehicleInfo.vehicle_name.contains(vehicle_name))
    if brand:
        filters.append(VehicleInfo.brand.contains(brand))
    where = and_(*filters)
    offset = (page - 1) * page_size
    total_r = await db.execute(select(func.count()).select_from(VehicleInfo).where(where))
    total = total_r.scalar() or 0
    stmt = select(VehicleInfo).where(where).offset(offset).limit(page_size).order_by(VehicleInfo.id.desc())
    result = await db.execute(stmt)
    items = list(result.scalars().all())
    data_items = [{
        "id": v.id, "vehicle_code": v.vehicle_code, "vehicle_name": v.vehicle_name,
        "vehicle_model": v.vehicle_model, "brand": v.brand, "year_model": v.year_model,
        "engine_model": v.engine_model, "description": v.description,
        "create_time": v.create_time, "update_time": v.update_time,
    } for v in items]
    return success_response(data=page_response(data_items, total, page, page_size))


@router.post("", response_model=dict)
async def create_vehicle(
    body: VehicleCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    existing = await db.execute(select(VehicleInfo).where(VehicleInfo.vehicle_code == body.vehicle_code))
    if existing.scalar_one_or_none():
        return success_response(data=None, message="整车编号已存在")
    vehicle = VehicleInfo(**body.model_dump())
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return success_response(data={
        "id": vehicle.id, "vehicle_code": vehicle.vehicle_code, "vehicle_name": vehicle.vehicle_name,
        "vehicle_model": vehicle.vehicle_model, "brand": vehicle.brand, "year_model": vehicle.year_model,
        "engine_model": vehicle.engine_model, "description": vehicle.description,
        "create_time": vehicle.create_time, "update_time": vehicle.update_time,
    })


@router.put("/{vehicle_id}", response_model=dict)
async def update_vehicle(
    vehicle_id: int, body: VehicleUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    r = await db.execute(select(VehicleInfo).where(VehicleInfo.id == vehicle_id, VehicleInfo.is_deleted == 0))
    vehicle = r.scalar_one_or_none()
    if not vehicle:
        return success_response(data=None, message="整车不存在")
    update_data = body.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(vehicle, k, v)
    await db.commit()
    await db.refresh(vehicle)
    return success_response(data={
        "id": vehicle.id, "vehicle_code": vehicle.vehicle_code, "vehicle_name": vehicle.vehicle_name,
        "vehicle_model": vehicle.vehicle_model, "brand": vehicle.brand, "year_model": vehicle.year_model,
        "engine_model": vehicle.engine_model, "description": vehicle.description,
        "create_time": vehicle.create_time, "update_time": vehicle.update_time,
    })


@router.delete("/{vehicle_id}", response_model=dict)
async def delete_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    r = await db.execute(select(VehicleInfo).where(VehicleInfo.id == vehicle_id, VehicleInfo.is_deleted == 0))
    vehicle = r.scalar_one_or_none()
    if not vehicle:
        return success_response(data=None, message="整车不存在")
    vehicle.is_deleted = 1
    await db.commit()
    return success_response(data=None, message="删除成功")


@router.get("/{vehicle_id}", response_model=dict)
async def get_vehicle(
    vehicle_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    r = await db.execute(select(VehicleInfo).where(VehicleInfo.id == vehicle_id, VehicleInfo.is_deleted == 0))
    vehicle = r.scalar_one_or_none()
    if not vehicle:
        return success_response(data=None, message="整车不存在")
    return success_response(data={
        "id": vehicle.id, "vehicle_code": vehicle.vehicle_code, "vehicle_name": vehicle.vehicle_name,
        "vehicle_model": vehicle.vehicle_model, "brand": vehicle.brand, "year_model": vehicle.year_model,
        "engine_model": vehicle.engine_model, "description": vehicle.description,
        "create_time": vehicle.create_time, "update_time": vehicle.update_time,
    })
