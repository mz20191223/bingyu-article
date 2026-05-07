import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import Website, PublishRecord, Product
from app.services.publish_service import publish_article
import time
import traceback as tb

app = create_app()
app.app_context().push()

try:
    print("=" * 60)
    print("完整测试 publish_article")
    print("=" * 60)

    title = "完整测试_" + str(int(time.time()))
    content = "完整测试内容"

    website_id = 6
    product_id = 1
    user_id = 1

    print(f"标题: {title}")
    print(f"网站ID: {website_id}, 产品ID: {product_id}")

    result = publish_article(
        product_id=product_id,
        website_ids=[website_id],
        title=title,
        content=content,
        model_id=None,
        title_template_id=None,
        content_template_id=None,
        user_id=user_id
    )

    print(f"\n返回结果: {result}")

    # 获取最新记录
    record = PublishRecord.query.filter_by(title=title).order_by(PublishRecord.id.desc()).first()
    if record:
        print(f"\n数据库记录:")
        print(f"  ID: {record.id}")
        print(f"  状态: {record.status}")
        print(f"  URL: {record.result_url}")
        print(f"  错误: {record.error_msg}")

except Exception as e:
    print(f"错误: {e}")
    tb.print_exc()