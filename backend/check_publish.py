import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db, PublishRecord, Website

app = create_app()

with app.app_context():
    # 获取最新的发布记录
    records = PublishRecord.query.filter(
        PublishRecord.status == 'success',
        PublishRecord.website_id == 6  # 有目网
    ).order_by(PublishRecord.publish_time.desc()).limit(5).all()

    print(f"=== 有目网最近发布记录 ===")
    if records:
        for i, record in enumerate(records, 1):
            print(f"\n记录{i}:")
            print(f"  ID: {record.id}")
            print(f"  标题: {record.title}")
            print(f"  网站: {record.website_name}")
            print(f"  状态: {record.status}")
            print(f"  发布时间: {record.publish_time}")
            print(f"  结果URL: {record.result_url}")
            print(f"  内容长度: {len(record.content)}")
            print(f"  img标签数: {record.content.count('<img')}")
    else:
        print("没有找到有目网的成功发布记录")
