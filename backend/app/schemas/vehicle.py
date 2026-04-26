from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VehicleCreate(BaseModel):
    vehicle_code: str
    vehicle_name: str
    vehicle_model: str = ""
    brand: str = ""
    year_model: str = ""
    engine_model: str = ""
    description: str = ""


class VehicleUpdate(BaseModel):
    vehicle_name: Optional[str] = None
    vehicle_model: Optional[str] = None
    brand: Optional[str] = None
    year_model: Optional[str] = None
    engine_model: Optional[str] = None
    description: Optional[str] = None


class VehicleResponse(BaseModel):
    id: int
    vehicle_code: str
    vehicle_name: str
    vehicle_model: str
    brand: str
    year_model: str
    engine_model: str
    description: str
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True
