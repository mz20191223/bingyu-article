import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import PublishRecord

app = create_app()
with app.app_context():
    record = PublishRecord.query.get(74)
    if record:
        print(f"发布记录 ID: {record.id}")
        print(f"标题: {record.title}")
        print(f"状态: {record.status}")
        print(f"文章链接: {record.result_url}")
        print(f"错误信息: {record.error_msg}")
        print(f"发布时间: {record.publish_time}")
        print(f"网站ID: {record.website_id}")
        print(f"网站名称: {record.website_name}")
    else:
        print("记录不存在")