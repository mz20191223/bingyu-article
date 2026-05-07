"""
查看网站配置信息
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Website

app = create_app()

with app.app_context():
    websites = Website.query.all()
    print("网站配置列表:")
    for w in websites:
        print(f"ID: {w.id}, 名称: {w.name}")
        print(f"  账号: {w.username}, 密码: {w.password}")
        print(f"  登录URL: {w.login_url}")
        print(f"  发布URL: {w.publish_url}")
        print()