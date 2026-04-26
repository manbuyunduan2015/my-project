#!/usr/bin/env python3
"""Seed script to insert initial roles and admin user."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.models.base import engine
from app.core.security import get_password_hash


async def seed():
    async with engine.connect() as conn:
        # Insert roles
        await conn.execute(text(
            "INSERT IGNORE INTO sys_role (role_name, role_desc) VALUES "
            "('admin', '超级管理员，拥有全部增删改查权限'), "
            "('viewer', '普通用户，仅拥有查看权限')"
        ))

        # Insert admin user (password: admin123)
        hashed = get_password_hash("admin123")
        await conn.execute(text(
            "INSERT IGNORE INTO sys_user (username, real_name, password, phone, email, status) "
            "VALUES ('admin', '系统管理员', :password, '', '', 1)"
        ), {"password": hashed})

        # Link admin to admin role
        await conn.execute(text(
            "INSERT IGNORE INTO sys_user_role (user_id, role_id) "
            "SELECT u.id, r.id FROM sys_user u, sys_role r "
            "WHERE u.username = 'admin' AND r.role_name = 'admin'"
        ))

        await conn.commit()
        print("Seed data inserted successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
