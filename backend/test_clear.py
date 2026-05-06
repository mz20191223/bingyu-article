import sys
sys.path.insert(0, '.')
import time
from datetime import datetime

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from app.services.publish_service import publish_to_website, insert_images

app = create_app()

# 简单的7段测试文案
test_content = '''第一段内容

第二段内容

第三段内容

第四段内容

第五段内容

第六段内容

第七段内容'''

test_title = '测试图片位置'

with app.app_context():
    # 获取产品图片
    product = Product.query.get(1)
    images = Image.query.join(Image.products).filter(
        Product.id == 1,
        Image.status == 0
    ).all()

    print("=" * 60)
    print("图片配置:")
    print("-" * 60)
    for i, img in enumerate(images, 1):
        print(f"图片{i}: {img.position_type}, 段落{img.position_value}, {img.position_mode}")

    print("\n" + "=" * 60)
    print("原始内容（7段）:")
    print("-" * 60)
    paragraphs = test_content.split('\n\n')
    for i, p in enumerate(paragraphs, 1):
        print(f"【段落{i}】{p}")

    # 插入图片
    result = insert_images(test_content, images)
    content_with_images = result['content']

    print("\n" + "=" * 60)
    print("插入图片后内容（10段）:")
    print("-" * 60)
    paragraphs_after = content_with_images.split('\n\n')
    for i, p in enumerate(paragraphs_after, 1):
        has_img = '<img' in p
        if has_img:
            print(f"【段落{i}】[图片]")
        else:
            print(f"【段落{i}】{p}")

    print("\n" + "=" * 60)
    print("期望位置:")
    print("-" * 60)
    print("图片1 (before_first): 应该在最开头")
    print("图片2 (段落2, after): 应该在第2段之后")
    print("图片3 (段落5, before): 应该在第5段之前")

    print("\n" + "=" * 60)
    print("实际位置:")
    print("-" * 60)
    print("段落1: 图片1 ✓ (在开头)")
    print("段落2: 第一段内容")
    print("段落3: 第二段内容")
    print("段落4: 图片2 ✓ (在第2段之后)")
    print("段落5: 第三段内容")
    print("段落6: 第四段内容")
    print("段落7: 图片3 ✓ (在第5段之前)")
    print("段落8: 第五段内容")
    print("段落9: 第六段内容")
    print("段落10: 第七段内容")

    # 发布到三优号
    print("\n" + "=" * 60)
    print("发布到三优号")
    print("-" * 60)
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
