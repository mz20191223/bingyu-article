import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import PublishRecord

app = create_app()
with app.app_context():
    record = PublishRecord.query.get(77)
    if record:
        print(f"ID: {record.id}")
        print(f"标题: {record.title}")
        print(f"状态: {record.status}")
        print(f"文章链接: {record.result_url}")