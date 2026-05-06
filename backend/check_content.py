import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import create_app
from app.models import db, PublishRecord

app = create_app()
with app.app_context():
    # 查看最新发布记录的内容
    record = PublishRecord.query.order_by(PublishRecord.id.desc()).first()
    if record:
        print(f"记录ID: {record.id}")
        print(f"网站: {record.website_name}")
        print(f"标题: {record.title}")
        print(f"\n内容（前500字符）:\n{record.content[:500]}")
        print(f"\n内容是否包含img: {'<img' in record.content}")
