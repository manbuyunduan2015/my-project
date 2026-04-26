from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base


class SysUser(Base):
    __tablename__ = "sys_user"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(64), unique=True, nullable=False, comment="用户名")
    real_name = Column(String(64), nullable=False, server_default="", comment="真实姓名")
    password = Column(String(128), nullable=False, comment="密码")
    phone = Column(String(20), nullable=False, server_default="", comment="手机号")
    email = Column(String(128), nullable=False, server_default="", comment="邮箱")
    status = Column(Integer, nullable=False, server_default="1", comment="状态: 1=启用, 0=停用")
    is_deleted = Column(Integer, nullable=False, server_default="0", comment="软删除")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    user_roles = relationship("SysUserRole", back_populates="user", lazy="selectin")

    @property
    def roles(self):
        return [ur.role.role_name for ur in self.user_roles]
