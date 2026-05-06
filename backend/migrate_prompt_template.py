import sys
sys.path.insert(0, '.')
from app import create_app
from app.models import db
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        print("开始创建提示词模板表...")

        try:
            result = db.session.execute(text("SHOW TABLES LIKE 'prompt_templates'"))
            if not result.fetchone():
                db.session.execute(text("""
                    CREATE TABLE prompt_templates (
                        id INT NOT NULL AUTO_INCREMENT,
                        name VARCHAR(100) NOT NULL,
                        prompt_content TEXT NOT NULL,
                        required_paragraphs INT DEFAULT 5,
                        business_type VARCHAR(50),
                        is_default INT DEFAULT 0,
                        status INT DEFAULT 0,
                        create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        PRIMARY KEY (id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """))
                print("✓ 创建 prompt_templates 表成功")
            else:
                print("○ prompt_templates 表已存在")

            result = db.session.execute(text("SHOW TABLES LIKE 'template_product'"))
            if not result.fetchone():
                db.session.execute(text("""
                    CREATE TABLE template_product (
                        template_id INT NOT NULL,
                        product_id INT NOT NULL,
                        PRIMARY KEY (template_id, product_id),
                        FOREIGN KEY (template_id) REFERENCES prompt_templates(id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """))
                print("✓ 创建 template_product 表成功")
            else:
                print("○ template_product 表已存在")

            db.session.commit()
            print("迁移完成!")
        except Exception as e:
            db.session.rollback()
            print(f"✗ 迁移失败: {e}")

if __name__ == "__main__":
    migrate()
