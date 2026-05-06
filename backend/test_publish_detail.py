import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from app.services.publish_service import insert_images

app = create_app()
with app.app_context():
    # 测试用的文章内容
    test_content = '''【京东返利：为什么你需要一个靠谱的返利工具？】
在电商行业蓬勃发展的今天，京东凭借其正品保障，物流优势和品类丰富度，成为无数消费者购物的首选平台。

【高省返利APP：京东官方合作，返利更安心】
为什么说"高省返利APP"是京东返利工具中的佼佼者？

【返利力度真实透明，告别"套路优惠"】
高省返利APP坚持"真实返利、无套路"原则。'''

    # 获取产品"高省"的图片
    product = Product.query.get(1)
    images = Image.query.join(Image.products).filter(
        Product.id == 1,
        Image.status == 0
    ).all()

    # 测试图片插入
    website_ids = [6, 7, 8]  # 三个网站的ID
    result = insert_images(test_content, images, website_ids)

    # 详细检查内容
    print("=== 检查插入后的内容 ===")
    print(f"总字符数: {len(result['content'])}")

    # 查找所有img标签
    import re
    img_tags = re.findall(r'<img[^>]+>', result['content'])
    print(f"\n找到 {len(img_tags)} 个img标签:")
    for i, tag in enumerate(img_tags, 1):
        print(f"  {i}. {tag}")

    # 检查第一张图片URL是否完整
    print("\n=== 验证图片URL完整性 ===")
    for img in images:
        expected_url = img.url
        if expected_url in result['content']:
            print(f"✓ URL完整存在: {expected_url}")
        else:
            print(f"✗ URL不完整或缺失: {expected_url}")
            # 检查截断情况
            truncated = expected_url[:50]
            if truncated in result['content']:
                print(f"  检测到截断: {truncated}...")

    # 保存到数据库测试
    print("\n=== 保存到数据库测试 ===")
    website = Website.query.get(6)  # 有目网

    record = PublishRecord(
        product_id=1,
        product_name=product.name,
        website_id=6,
        website_name=website.name,
        title='测试文章20260430',
        content=result['content'],
        status='pending'
    )
    db.session.add(record)
    db.session.commit()

    # 重新读取验证
    saved_record = PublishRecord.query.get(record.id)
    print(f"保存成功，ID: {saved_record.id}")
    print(f"保存内容长度: {len(saved_record.content)}")
    print(f"保存内容中的img标签数量: {saved_record.content.count('<img')}")

    # 再次验证URL
    for img in images:
        if img.url in saved_record.content:
            print(f"✓ 保存后URL仍完整: {img.url}")
        else:
            print(f"✗ 保存后URL缺失: {img.url}")
