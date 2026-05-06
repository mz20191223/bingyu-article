import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db, Product, Image

app = create_app()
with app.app_context():
    # 获取产品"高省"的最新图片配置
    product = Product.query.get(1)
    images = Image.query.join(Image.products).filter(
        Product.id == 1,
        Image.status == 0
    ).all()

    print(f"=== 产品: {product.name} (ID: {product.id}) ===")
    print(f"关联图片数量: {len(images)}")
    print()

    for i, img in enumerate(images, 1):
        print(f"图片{i}:")
        print(f"  ID: {img.id}")
        print(f"  URL: {img.url}")
        print(f"  位置类型 (position_type): {img.position_type}")
        print(f"  位置值 (position_value): {img.position_value}")
        print(f"  位置模式 (position_mode): {img.position_mode}")
        print()

    # 如果只有2张图但用户说有第3张，提示用户上传
    if len(images) < 3:
        print(f"注意：当前只有 {len(images)} 张图片关联到该产品")
        print("如果你需要第3张图片，请先在图片管理中上传并关联到产品")
