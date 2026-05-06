import sys
sys.path.insert(0, '.')
import time
from datetime import datetime

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from app.services.publish_service import publish_to_website, insert_images

app = create_app()

# 简单的7段测试文案
test_content = '''这是第一段内容

这是第二段内容

这是第三段内容

这是第四段内容

这是第五段内容

这是第六段内容

这是第七段内容'''

test_title = '测试图片位置'

with app.app_context():
    # 获取产品图片
    product = Product.query.get(1)
    images = Image.query.join(Image.products).filter(
        Product.id == 1,
        Image.status == 0
    ).all()

    print(f"=== 图片配置 ===")
    for i, img in enumerate(images, 1):
        print(f"  图片{i}: position_type={img.position_type}, position_value={img.position_value}, position_mode={img.position_mode}")

    print("\n=== 原始段落 ===")
    paragraphs = test_content.split('\n\n')
    for i, p in enumerate(paragraphs, 1):
        print(f"  段落{i}: {p}")

    # 插入图片
    result = insert_images(test_content, images)
    content_with_images = result['content']

    print("\n=== 插入后段落 ===")
    paragraphs_after = content_with_images.split('\n\n')
    for i, p in enumerate(paragraphs_after, 1):
        has_img = '<img' in p
        img_marker = " [含图片]" if has_img else ""
        print(f"  段落{i}: {p}{img_marker}")

    # 发布到三优号
    print("\n=== 发布到三优号 ===")
    website = Website.query.get(7)
    record = PublishRecord(
        product_id=1,
        product_name=product.name,
        website_id=7,
        website_name=website.name,
        title=test_title,
        content=content_with_images,
        status='pending'
    )
    db.session.add(record)
    db.session.commit()

    try:
        result = publish_to_website(record, website, test_title, content_with_images)
        record.status = 'success'
        record.result_url = result.get('url')
        record.publish_time = datetime.now()
        print(f"✓ {website.name} 发布成功")
    except Exception as e:
        record.status = 'failed'
        record.error_msg = str(e)
        print(f"✗ {website.name} 发布失败: {e}")
    
    db.session.commit()
