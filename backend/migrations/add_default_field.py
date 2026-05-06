import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db

def upgrade():
    from sqlalchemy import text
    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("SHOW COLUMNS FROM products LIKE 'is_default'"))
            if result.fetchone():
                print('products.is_default column already exists')
            else:
                conn.execute(text('ALTER TABLE products ADD COLUMN is_default INT DEFAULT 0'))
                print('Added is_default column to products table')
    except Exception as e:
        print(f'Error adding products.is_default: {e}')

    try:
        with db.engine.connect() as conn:
            result = conn.execute(text("SHOW COLUMNS FROM websites LIKE 'is_default'"))
            if result.fetchone():
                print('websites.is_default column already exists')
            else:
                conn.execute(text('ALTER TABLE websites ADD COLUMN is_default INT DEFAULT 0'))
                print('Added is_default column to websites table')
    except Exception as e:
        print(f'Error adding websites.is_default: {e}')

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        upgrade()
        print('Migration completed')
