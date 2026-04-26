from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.models.base import Base


class VehicleInfo(Base):
    __tablename__ = "vehicle_info"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="整车ID")
    vehicle_code = Column(String(64), unique=True, nullable=False, comment="整车编号")
    vehicle_name = Column(String(128), nullable=False, comment="整车名称")
    vehicle_model = Column(String(128), nullable=False, server_default="", comment="整车型号")
    brand = Column(String(64), nullable=False, server_default="", comment="品牌")
    year_model = Column(String(16), nullable=False, server_default="", comment="年款")
    engine_model = Column(String(128), nullable=False, server_default="", comment="发动机型号")
    description = Column(Text, nullable=False, server_default="", comment="描述")
    is_deleted = Column(Integer, nullable=False, server_default="0", comment="软删除")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
