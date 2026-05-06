import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from sqlalchemy.orm import joinedload

app = create_app()
with app.app_context():
    # 查看网站配置
    websites = Website.query.all()
    print("=== 网站配置 ===")
    for w in websites:
        print(f"ID: {w.id}, 名称: {w.name}")
        print(f"  登录URL: {w.login_url}")
        print(f"  发布URL: {w.publish_url}")
        print()

    # 查看产品图片 - 使用正确的查询方式
    products = Product.query.all()
    print("\n=== 产品和图片 ===")
    for p in products:
        images = Image.query.join(Image.products).filter(Product.id == p.id, Image.status == 0).all()
        if images:
            print(f"产品: {p.name}, ID: {p.id}")
            print(f"  关联图片数量: {len(images)}")
            for img in images:
                print(f"    - URL: {img.url}")
                print(f"      位置类型: {img.position_type}, 位置值: {img.position_value}, 位置模式: {img.position_mode}")
