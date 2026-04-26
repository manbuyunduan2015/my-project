from typing import Optional, Type, TypeVar, Generic, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.sql import Select
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, page: int = 1, page_size: int = 10
    ) -> tuple[List[ModelType], int]:
        offset = (page - 1) * page_size
        count_stmt = select(func.count(self.model.id))
        total_result = await db.execute(count_stmt)
        total = total_result.scalar() or 0
        stmt = select(self.model).offset(offset).limit(page_size).order_by(self.model.id.desc())
        result = await db.execute(stmt)
        items = list(result.scalars().all())
        return items, total

    async def get_multi_filtered(
        self,
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[list] = None,
    ) -> tuple[List[ModelType], int]:
        offset = (page - 1) * page_size
        where_clause = and_(*filters) if filters else True
        count_stmt = select(func.count(self.model.id)).where(where_clause)
        total_result = await db.execute(count_stmt)
        total = total_result.scalar() or 0
        stmt = (
            select(self.model)
            .where(where_clause)
            .offset(offset)
            .limit(page_size)
            .order_by(self.model.id.desc())
        )
        result = await db.execute(stmt)
        items = list(result.scalars().all())
        return items, total

    async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: dict) -> ModelType:
        for key, value in obj_in.items():
            if value is not None:
                setattr(db_obj, key, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, id: int) -> bool:
        obj = await self.get_by_id(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return True
        return False
