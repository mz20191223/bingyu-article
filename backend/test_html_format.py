import sys
sys.path.insert(0, '.')
import time
from datetime import datetime

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from app.services.publish_service import publish_to_website, insert_images

app = create_app()

# 简单的7段测试文案，确保段落分开
test_content = '''<p>第一段内容</p>
<p>第二段内容</p>
<p>第三段内容</p>
<p>第四段内容</p>
<p>第五段内容</p>
<p>第六段内容</p>
<p>第七段内容</p>'''

test_title = '测试图片位置'

with app.app_context():
    # 获取产品图片
    product = Product.query.get(1)
    images = Image.query.join(Image.products).filter(
        Product.id == 1,
        Image.status == 0
    ).all()

    print("图片配置:")
    for i, img in enumerate(images, 1):
        print(f"图片{i}: {img.position_type}, 段落{img.position_value}, {img.position_mode}")

    print("\n原始内容:")
    print(test_content)

    # 插入图片
    result = insert_images(test_content, images)
    content_with_images = result['content']

    print("\n插入图片后内容:")
    print(content_with_images)

    # 发布到三优号
    print("\n发布到三优号...")
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
        print(f"✓ 发布成功")
    except Exception as e:
        record.status = 'failed'
        record.error_msg = str(e)
        print(f"✗ 发布失败: {e}")
    
    db.session.commit()
