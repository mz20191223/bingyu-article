from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    from sqlalchemy import text
    
    try:
        # 添加 conclusion_text 字段
        db.engine.execute(text('ALTER TABLE prompt_templates ADD COLUMN conclusion_text TEXT;'))
        print("Successfully added conclusion_text column")
    except Exception as e:
        print(f"Error: {e}")
        
    try:
        # 添加 text_overlay 字段到 images 表（如果不存在）
        db.engine.execute(text('ALTER TABLE images ADD COLUMN text_overlay TEXT;'))
        print("Successfully added text_overlay column")
    except Exception as e:
        print(f"Error: {e}")
        
    try:
        # 添加 composite_url 字段到 images 表（如果不存在）
        db.engine.execute(text('ALTER TABLE images ADD COLUMN composite_url VARCHAR(500);'))
        print("Successfully added composite_url column")
    except Exception as e:
        print(f"Error: {e}")