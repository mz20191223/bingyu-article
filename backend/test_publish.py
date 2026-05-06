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

    print(f"产品: {product.name}")
    print(f"图片数量: {len(images)}")
    for img in images:
        print(f"  - URL: {img.url}")
        print(f"    位置类型: {img.position_type}, 位置值: {img.position_value}, 位置模式: {img.position_mode}")

    print(f"\n原始内容:\n{test_content}")

    # 测试图片插入
    website_ids = [6, 7, 8]  # 三个网站的ID
    result = insert_images(test_content, images, website_ids)

    print(f"\n=== 插入图片后的内容 ===")
    print(result['content'])

    print(f"\n内容是否包含img标签: {'<img' in result['content']}")

    # 检查每个网站的图片插入情况
    print(f"\n=== 各网站发布的内容预览 ===")
    for wid in website_ids:
        website = Website.query.get(wid)
        print(f"\n{website.name} (ID: {wid}):")
        print(f"  内容长度: {len(result['content'])} 字符")
        print(f"  img标签数量: {result['content'].count('<img')}")
