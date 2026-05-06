import sys
sys.path.insert(0, '.')
import time
import json
from datetime import datetime

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from app.services.publish_service import publish_to_website, insert_images

app = create_app()

# 测试用的文章内容
test_content = '''【京东返利：为什么你需要一个靠谱的返利工具？】
在电商行业蓬勃发展的今天，京东凭借其正品保障，物流优势和品类丰富度，成为无数消费者购物的首选平台。

【高省返利APP：京东官方合作，返利更安心】
为什么说"高省返利APP"是京东返利工具中的佼佼者？

【返利力度真实透明，告别"套路优惠"】
高省返利APP坚持"真实返利、无套路"原则'''

test_title = '京东返利app哪个最好？京东官方返利app哪个最好'

with app.app_context():
    # 获取产品"高省"的图片
    product = Product.query.get(1)
    images = Image.query.join(Image.products).filter(
        Product.id == 1,
        Image.status == 0
    ).all()

    # 插入图片
    website_ids = [6, 7, 8]
    result = insert_images(test_content, images, website_ids)
    content_with_images = result['content']

    print(f"=== 图片插入结果 ===")
    print(f"图片数量: {len(images)}")
    print(f"内容长度: {len(content_with_images)}")
    print(f"img标签数量: {content_with_images.count('<img')}")

    # 创建发布记录
    print("\n=== 创建发布记录 ===")
    records = []
    for wid in website_ids:
        website = Website.query.get(wid)
        record = PublishRecord(
            product_id=1,
            product_name=product.name,
            website_id=wid,
            website_name=website.name,
            title=test_title,
            content=content_with_images,
            status='pending'
        )
        db.session.add(record)
        records.append(record)

    db.session.commit()
    print(f"创建了 {len(records)} 条发布记录")

    # 提示用户确认是否继续测试浏览器发布
    print("\n=== 浏览器自动化测试 ===")
    print("准备测试三个网站的浏览器自动化发布功能...")
    print("即将打开浏览器窗口，请确保屏幕可以观察到测试过程")
    print("按 Ctrl+C 可以取消测试")
    time.sleep(3)

    # 测试第一个网站
    for i, record in enumerate(records):
        website = Website.query.get(record.website_id)
        print(f"\n--- 测试 {i+1}/{len(records)}: {website.name} ---")

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
        time.sleep(2)

    # 总结结果
    print("\n=== 测试结果汇总 ===")
    for record in records:
        status_icon = "✓" if record.status == 'success' else "✗"
        print(f"{status_icon} {record.website_name}: {record.status}")
        if record.result_url:
            print(f"   URL: {record.result_url}")
        if record.error_msg:
            print(f"   错误: {record.error_msg}")

    # 验证保存的内容
    print("\n=== 数据库内容验证 ===")
    for record in records:
        has_img = '<img' in record.content
        img_count = record.content.count('<img')
        print(f"{record.website_name}: 包含{'是' if has_img else '否'} img标签, 数量: {img_count}")
