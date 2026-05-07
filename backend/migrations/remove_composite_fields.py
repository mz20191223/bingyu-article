"""
迁移脚本：删除图片表中不再使用的文字叠加相关字段
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    # 检查并删除 text_overlay 字段
    print("检查 text_overlay 字段...")
    result = db.engine.execute("SHOW COLUMNS FROM images")
    columns = [col[0] for col in result.fetchall()]
    
    if 'text_overlay' in columns:
        print("删除 text_overlay 字段...")
        db.engine.execute("ALTER TABLE images DROP COLUMN text_overlay")
        print("text_overlay 字段删除成功")
    else:
        print("text_overlay 字段不存在")
    
    if 'composite_url' in columns:
        print("删除 composite_url 字段...")
        db.engine.execute("ALTER TABLE images DROP COLUMN composite_url")
        print("composite_url 字段删除成功")
    else:
        print("composite_url 字段不存在")
    
    print("\n迁移完成！")