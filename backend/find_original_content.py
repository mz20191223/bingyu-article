import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db, PublishRecord

app = create_app()
with app.app_context():
    # 查看最近一条包含图片的成功发布记录
    records = PublishRecord.query.filter(
        PublishRecord.content.contains('<img')
    ).order_by(PublishRecord.id.desc()).limit(3).all()

    print(f"找到 {len(records)} 条包含图片的发布记录\n")

    for record in records:
        print(f"=== 记录ID: {record.id} - {record.website_name} ===")
        print(f"标题: {record.title}")
        print(f"内容长度: {len(record.content)} 字符")
        print(f"img标签数量: {record.content.count('<img')}")
        print(f"\n完整内容:")
        print(record.content)
        print("\n" + "="*80 + "\n")
