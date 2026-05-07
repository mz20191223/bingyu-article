"""
检查数据库中的用户信息
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, SysUser

app = create_app()

with app.app_context():
    users = SysUser.query.all()
    print("数据库中的用户列表:")
    for user in users:
        print(f"ID: {user.user_id}, 用户名: {user.username}, 密码: {user.password}")
