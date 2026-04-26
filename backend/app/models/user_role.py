from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class SysUserRole(Base):
    __tablename__ = "sys_user_role"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="关联ID")
    user_id = Column(Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), nullable=False, comment="用户ID")
    role_id = Column(Integer, ForeignKey("sys_role.id", ondelete="CASCADE"), nullable=False, comment="角色ID")

    user = relationship("SysUser", back_populates="user_roles", lazy="selectin")
    role = relationship("SysRole", back_populates="user_roles", lazy="selectin")
