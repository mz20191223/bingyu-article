import sys
sys.path.insert(0, '.')
from app import create_app
from app.models import db
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        print("开始数据库迁移...")

        try:
            # 创建 content_template_product 表
            result = db.session.execute(text("SHOW TABLES LIKE 'content_template_product'"))
            if not result.fetchone():
                db.session.execute(text("CREATE TABLE content_template_product (template_id INT NOT NULL, product_id INT NOT NULL, PRIMARY KEY (template_id, product_id), FOREIGN KEY (template_id) REFERENCES content_prompt_templates(id) ON DELETE CASCADE, FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE)"))
                print("创建 content_template_product 表成功")
            else:
                print("content_template_product 表已存在")

            # 创建 title_template_product 表
            result = db.session.execute(text("SHOW TABLES LIKE 'title_template_product'"))
            if not result.fetchone():
                db.session.execute(text("CREATE TABLE title_template_product (template_id INT NOT NULL, product_id INT NOT NULL, PRIMARY KEY (template_id, product_id), FOREIGN KEY (template_id) REFERENCES title_prompt_templates(id) ON DELETE CASCADE, FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE)"))
                print("创建 title_template_product 表成功")
            else:
                print("title_template_product 表已存在")

            # 旧字段由外键约束保护，保留即可，不影响新功能

            db.session.commit()
            print("迁移完成!")
        except Exception as e:
            db.session.rollback()
            print(f"失败: {e}")

if __name__ == "__main__":
    migrate()
