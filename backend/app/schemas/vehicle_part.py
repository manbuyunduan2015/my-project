from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RelationCreate(BaseModel):
    vehicle_id: int
    part_id: int
    quantity: int = 1
    position_name: str = ""
    remark: str = ""


class RelationUpdate(BaseModel):
    quantity: Optional[int] = None
    position_name: Optional[str] = None
    remark: Optional[str] = None


class RelationResponse(BaseModel):
    id: int
    vehicle_id: int
    part_id: int
    quantity: int
    position_name: str
    remark: str
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class BOMPartDetail(BaseModel):
    relation_id: int
    part_id: int
    part_code: str
    part_name: str
    category: str
    quantity: int
    position_name: str
    remark: str


class BOMResponse(BaseModel):
    vehicle: dict
    parts: list[BOMPartDetail]
    total_parts: int
