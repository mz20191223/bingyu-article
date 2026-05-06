from app import create_app
from app.models import db, text

def migrate():
    app = create_app()
    with app.app_context():
        print("=" * 60)
        print("开始数据库迁移 - 创建多对多关系表...")
        print("=" * 60)

        try:
            # 创建 content_template_product 表
            result = db.session.execute(text("SHOW TABLES LIKE 'content_template_product'"))
            if not result.fetchone():
                db.session.execute(text("""
                    CREATE TABLE content_template_product (
                        template_id INT NOT NULL,
                        product_id INT NOT NULL,
                        PRIMARY KEY (template_id, product_id),
                        FOREIGN KEY (template_id) REFERENCES content_prompt_templates(id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                    )
                """))
                print("✓ 创建 content_template_product 表成功")
            else:
                print("○ content_template_product 表已存在")

            # 创建 title_template_product 表
            result = db.session.execute(text("SHOW TABLES LIKE 'title_template_product'"))
            if not result.fetchone():
                db.session.execute(text("""
                    CREATE TABLE title_template_product (
                        template_id INT NOT NULL,
                        product_id INT NOT NULL,
                        PRIMARY KEY (template_id, product_id),
                        FOREIGN KEY (template_id) REFERENCES title_prompt_templates(id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                    )
                """))
                print("✓ 创建 title_template_product 表成功")
            else:
                print("○ title_template_product 表已存在")

            # 移除旧的 product_id 字段（如果存在）
            result = db.session.execute(text("SHOW COLUMNS FROM content_prompt_templates LIKE 'product_id'"))
            if result.fetchone():
                db.session.execute(text("ALTER TABLE content_prompt_templates DROP COLUMN product_id"))
                print("✓ content_prompt_templates 表已移除旧的 product_id 字段")
            else:
                print("○ content_prompt_templates 表没有旧的 product_id 字段")

            result = db.session.execute(text("SHOW COLUMNS FROM title_prompt_templates LIKE 'product_id'"))
            if result.fetchone():
                db.session.execute(text("ALTER TABLE title_prompt_templates DROP COLUMN product_id"))
                print("✓ title_prompt_templates 表已移除旧的 product_id 字段")
            else:
                print("○ title_prompt_templates 表没有旧的 product_id 字段")

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
