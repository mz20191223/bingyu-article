from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    from sqlalchemy import text
    
    try:
        # 添加 parameters 字段到 models 表
        db.engine.execute(text('ALTER TABLE models ADD COLUMN parameters TEXT;'))
        print("Successfully added parameters column to models table")
    except Exception as e:
        print(f"Error: {e}")