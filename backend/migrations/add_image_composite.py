import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db

app = create_app()

with app.app_context():
    # 添加 text_overlay 和 composite_url 字段
    try:
        # 检查字段是否已存在
        inspector = db.inspect(db.engine)
        columns = inspector.get_columns('images')
        column_names = [col['name'] for col in columns]
        
        if 'text_overlay' not in column_names:
            print("Adding text_overlay column...")
            db.engine.execute("ALTER TABLE images ADD COLUMN text_overlay TEXT")
        
        if 'composite_url' not in column_names:
            print("Adding composite_url column...")
            db.engine.execute("ALTER TABLE images ADD COLUMN composite_url VARCHAR(500)")
        
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Migration failed: {e}")
        import traceback
        traceback.print_exc()