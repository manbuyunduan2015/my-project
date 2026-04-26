from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.models.base import get_async_session
from app.models.vehicle_part import VehiclePartRelation
from app.models.vehicle import VehicleInfo
from app.models.part import PartInfo
from app.schemas.vehicle_part import RelationCreate, RelationUpdate
from app.core.deps import require_admin, get_current_user
from app.utils.response import success_response, page_response

router = APIRouter()


@router.get("/relations", response_model=dict)
async def list_relations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    vehicle_id: int = Query(None),
    part_id: int = Query(None),
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    filters = []
    if vehicle_id:
        filters.append(VehiclePartRelation.vehicle_id == vehicle_id)
    if part_id:
        filters.append(VehiclePartRelation.part_id == part_id)
    where = and_(*filters) if filters else True
    offset = (page - 1) * page_size
    total_r = await db.execute(select(func.count(VehiclePartRelation.id)).where(where))
    total = total_r.scalar() or 0
    stmt = (
        select(VehiclePartRelation).where(where).offset(offset).limit(page_size)
        .order_by(VehiclePartRelation.id.desc())
    )
    result = await db.execute(stmt)
    items = list(result.scalars().all())
    data = [{
        "id": r.id, "vehicle_id": r.vehicle_id, "part_id": r.part_id,
        "quantity": r.quantity, "position_name": r.position_name,
        "remark": r.remark, "create_time": r.create_time,
    } for r in items]
    return success_response(data=page_response(data, total, page, page_size))


@router.post("/relations", response_model=dict)
async def create_relation(
    body: RelationCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    existing = await db.execute(
        select(VehiclePartRelation).where(
            VehiclePartRelation.vehicle_id == body.vehicle_id,
            VehiclePartRelation.part_id == body.part_id,
        )
    )
    if existing.scalar_one_or_none():
        return success_response(data=None, message="该整车+零部件组合已存在")
    relation = VehiclePartRelation(**body.model_dump())
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return success_response(data={
        "id": relation.id, "vehicle_id": relation.vehicle_id, "part_id": relation.part_id,
        "quantity": relation.quantity, "position_name": relation.position_name,
        "remark": relation.remark, "create_time": relation.create_time,
    })


@router.put("/relations/{relation_id}", response_model=dict)
async def update_relation(
    relation_id: int, body: RelationUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    r = await db.execute(select(VehiclePartRelation).where(VehiclePartRelation.id == relation_id))
    relation = r.scalar_one_or_none()
    if not relation:
        return success_response(data=None, message="装配关系不存在")
    update_data = body.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(relation, k, v)
    await db.commit()
    await db.refresh(relation)
    return success_response(data={
        "id": relation.id, "vehicle_id": relation.vehicle_id, "part_id": relation.part_id,
        "quantity": relation.quantity, "position_name": relation.position_name,
        "remark": relation.remark, "create_time": relation.create_time,
    })


@router.delete("/relations/{relation_id}", response_model=dict)
async def delete_relation(
    relation_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    r = await db.execute(select(VehiclePartRelation).where(VehiclePartRelation.id == relation_id))
    relation = r.scalar_one_or_none()
    if not relation:
        return success_response(data=None, message="装配关系不存在")
    await db.delete(relation)
    await db.commit()
    return success_response(data=None, message="删除成功")


@router.get("/vehicles/{vehicle_id}/parts", response_model=dict)
async def get_vehicle_bom(
    vehicle_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    vehicle_r = await db.execute(select(VehicleInfo).where(VehicleInfo.id == vehicle_id, VehicleInfo.is_deleted == 0))
    vehicle = vehicle_r.scalar_one_or_none()
    if not vehicle:
        return success_response(data=None, message="整车不存在")
    result = await db.execute(
        select(VehiclePartRelation, PartInfo)
        .join(PartInfo, PartInfo.id == VehiclePartRelation.part_id)
        .where(VehiclePartRelation.vehicle_id == vehicle_id, PartInfo.is_deleted == 0)
    )
    rows = result.all()
    parts = []
    for rel, part in rows:
        parts.append({
            "relation_id": rel.id, "part_id": part.id,
            "part_code": part.part_code, "part_name": part.part_name,
            "category": part.category, "quantity": rel.quantity,
            "position_name": rel.position_name, "remark": rel.remark,
        })
    return success_response(data={
        "vehicle": {"id": vehicle.id, "vehicle_code": vehicle.vehicle_code, "vehicle_name": vehicle.vehicle_name},
        "parts": parts,
        "total_parts": len(parts),
    })


@router.get("/parts/{part_id}/vehicles", response_model=dict)
async def get_part_vehicles(
    part_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    part_r = await db.execute(select(PartInfo).where(PartInfo.id == part_id, PartInfo.is_deleted == 0))
    part = part_r.scalar_one_or_none()
    if not part:
        return success_response(data=None, message="零部件不存在")
    result = await db.execute(
        select(VehiclePartRelation, VehicleInfo)
        .join(VehicleInfo, VehicleInfo.id == VehiclePartRelation.vehicle_id)
        .where(VehiclePartRelation.part_id == part_id, VehicleInfo.is_deleted == 0)
    )
    rows = result.all()
    vehicles = []
    for rel, vehicle in rows:
        vehicles.append({
            "relation_id": rel.id, "vehicle_id": vehicle.id,
            "vehicle_code": vehicle.vehicle_code, "vehicle_name": vehicle.vehicle_name,
            "quantity": rel.quantity, "position_name": rel.position_name,
        })
    return success_response(data={
        "part": {"id": part.id, "part_code": part.part_code, "part_name": part.part_name},
        "vehicles": vehicles,
        "total_vehicles": len(vehicles),
    })
