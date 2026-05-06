import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import create_app
from app.models import db, Image, Product

app = create_app()
with app.app_context():
    # 检查高省关联的图片
    product = Product.query.get(1)
    print(f"产品: {product.name}")

    # 查询关联该产品的图片
    images = Image.query.join(Image.products).filter(
        Image.status == 0,
        Product.id == 1
    ).all()

    print(f"找到 {len(images)} 张图片:")
    for img in images:
        print(f"  ID:{img.id}")
        print(f"    URL: {img.url}")
        print(f"    position_type: {img.position_type}")
        print(f"    position_value: {img.position_value}")
        print(f"    position_mode: {img.position_mode}")

    # 模拟插入内容
    content = '''第一段内容
第二段内容
第三段内容'''

    print(f"\n原始内容:\n{content}")

    for img in images:
        img_html = f'<p><img src="{img.url}" /></p>'
        print(f"\n图片HTML: {img_html}")

        if img.position_type == 'before_first':
            content = img_html + content
        elif img.position_type == 'custom':
            paragraphs = content.split('\n')
            pos = min(img.position_value, len(paragraphs)-1) if paragraphs else 0
            if img.position_mode == 'before':
                paragraphs.insert(pos, img_html)
            else:
                paragraphs.insert(pos+1, img_html)
            content = '\n'.join(paragraphs)

    print(f"\n插入后内容:\n{content}")
