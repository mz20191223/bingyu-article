import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import PublishRecord

app = create_app()
with app.app_context():
    record = PublishRecord.query.get(82)
    if record:
        print(f"ID: {record.id}")
        print(f"标题: {record.title}")
        print(f"状态: {record.status}")
        print(f"返回链接: {record.result_url}")
        print(f"错误信息: {record.error_msg}")
    else:
        print("记录不存在")