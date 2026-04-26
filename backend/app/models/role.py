from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base


class SysRole(Base):
    __tablename__ = "sys_role"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="角色ID")
    role_name = Column(String(32), unique=True, nullable=False, comment="角色名称")
    role_desc = Column(String(128), nullable=False, server_default="", comment="角色描述")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")

    user_roles = relationship("SysUserRole", back_populates="role", lazy="selectin")
