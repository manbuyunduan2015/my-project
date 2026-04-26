from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.models.base import Base


class VehiclePartRelation(Base):
    __tablename__ = "vehicle_part_relation"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="关联ID")
    vehicle_id = Column(Integer, ForeignKey("vehicle_info.id", ondelete="CASCADE"), nullable=False, comment="整车ID")
    part_id = Column(Integer, ForeignKey("part_info.id", ondelete="CASCADE"), nullable=False, comment="零部件ID")
    quantity = Column(Integer, nullable=False, server_default="1", comment="装配数量")
    position_name = Column(String(128), nullable=False, server_default="", comment="装配位置")
    remark = Column(String(256), nullable=False, server_default="", comment="备注")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
