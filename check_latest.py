import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import PublishRecord

app = create_app()
with app.app_context():
    records = PublishRecord.query.order_by(PublishRecord.id.desc()).limit(5).all()
    for r in records:
        print(f"ID: {r.id}, 标题: {r.title[:30]}..., URL: {r.result_url}")