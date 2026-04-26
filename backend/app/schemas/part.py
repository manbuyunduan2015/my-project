from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class PartCreate(BaseModel):
    part_code: str
    part_name: str
    category: str = ""
    spec_model: str = ""
    material: str = ""
    supplier: str = ""
    unit: str = ""
    price: Decimal = Decimal("0.00")
    stock_qty: int = 0
    safe_stock: int = 0
    description: str = ""


class PartUpdate(BaseModel):
    part_name: Optional[str] = None
    category: Optional[str] = None
    spec_model: Optional[str] = None
    material: Optional[str] = None
    supplier: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[Decimal] = None
    stock_qty: Optional[int] = None
    safe_stock: Optional[int] = None
    description: Optional[str] = None


class PartResponse(BaseModel):
    id: int
    part_code: str
    part_name: str
    category: str
    spec_model: str
    material: str
    supplier: str
    unit: str
    price: Decimal
    stock_qty: int
    safe_stock: int
    low_stock: bool = False
    description: str
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True
