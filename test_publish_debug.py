import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import Website, PublishRecord
from app.services.publish_service import publish_to_website
import time

app = create_app()
with app.app_context():
    try:
        print("=" * 50)
        print("直接调用 publish_to_website 测试")
        print("=" * 50)

        title = "调试测试_" + str(int(time.time()))
        content = "调试测试内容"

        website = Website.query.get(6)

        # 创建一个假的 record
        record = PublishRecord(
            product_id=1,
            product_name='测试',
            website_id=6,
            website_name='有目网',
            title=title,
            content=content,
            status='pending'
        )
        db.session.add(record)
        db.session.commit()

        print(f"标题: {title}")
        print(f"开始发布...")

        result = publish_to_website(record, website, title, content)

        print(f"\n返回结果: {result}")
        print(f"URL: {result.get('url')}")

        # 检查记录
        db.session.refresh(record)
        print(f"\n数据库记录:")
        print(f"  status: {record.status}")
        print(f"  result_url: {record.result_url}")
        print(f"  error_msg: {record.error_msg}")

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()