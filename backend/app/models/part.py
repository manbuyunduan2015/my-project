from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, func
from app.models.base import Base


class PartInfo(Base):
    __tablename__ = "part_info"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="零部件ID")
    part_code = Column(String(64), unique=True, nullable=False, comment="零件编号")
    part_name = Column(String(128), nullable=False, comment="零件名称")
    category = Column(String(64), nullable=False, server_default="", comment="零件类别")
    spec_model = Column(String(128), nullable=False, server_default="", comment="规格型号")
    material = Column(String(128), nullable=False, server_default="", comment="材质")
    supplier = Column(String(128), nullable=False, server_default="", comment="供应商")
    unit = Column(String(16), nullable=False, server_default="", comment="单位")
    price = Column(Numeric(10, 2), nullable=False, server_default="0.00", comment="单价")
    stock_qty = Column(Integer, nullable=False, server_default="0", comment="库存数量")
    safe_stock = Column(Integer, nullable=False, server_default="0", comment="安全库存")
    description = Column(Text, nullable=False, server_default="", comment="描述")
    is_deleted = Column(Integer, nullable=False, server_default="0", comment="软删除")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
