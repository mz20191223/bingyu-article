"""
数据库迁移脚本：为 ContentPromptTemplate 和 TitlePromptTemplate 添加 product_id 字段
"""
import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("开始数据库迁移...")
        print("=" * 60)

        try:
            result = db.session.execute(text("SHOW COLUMNS FROM content_prompt_templates LIKE 'product_id'"))
            if not result.fetchone():
                db.session.execute(text("ALTER TABLE content_prompt_templates ADD COLUMN product_id INT NULL AFTER name"))
                print("✓ content_prompt_templates 表已添加 product_id 字段")
            else:
                print("○ content_prompt_templates 表 product_id 字段已存在")

            result = db.session.execute(text("SHOW COLUMNS FROM title_prompt_templates LIKE 'product_id'"))
            if not result.fetchone():
                db.session.execute(text("ALTER TABLE title_prompt_templates ADD COLUMN product_id INT NULL AFTER name"))
                print("✓ title_prompt_templates 表已添加 product_id 字段")
            else:
                print("○ title_prompt_templates 表 product_id 字段已存在")

            db.session.commit()

            print("=" * 60)
            print("数据库迁移完成！")
            print("=" * 60)

        except Exception as e:
            db.session.rollback()
            print(f"✗ 迁移失败: {e}")
            raise

if __name__ == '__main__':
    migrate()
