import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import db, Product, Image

app = create_app()

with app.app_context():
    # 获取产品"高省"的所有图片
    product = Product.query.get(1)
    
    # 查询方式1: 通过关联查询
    images1 = Image.query.join(Image.products).filter(
        Product.id == 1,
        Image.status == 0
    ).all()
    
    # 查询方式2: 直接查询所有关联图片
    images2 = product.images.filter(Image.status == 0).all()
    
    # 查询方式3: 查询所有图片然后过滤
    all_images = Image.query.filter(Image.status == 0).all()
    images3 = [img for img in all_images if product in img.products]
    
    print(f"=== 产品: {product.name} ===")
    print(f"方式1查询到 {len(images1)} 张图片")
    print(f"方式2查询到 {len(images2)} 张图片")
    print(f"方式3查询到 {len(images3)} 张图片")
    
    print("\n=== 所有图片详情 ===")
    for i, img in enumerate(images3, 1):
        print(f"\n图片{i}:")
        print(f"  ID: {img.id}")
        print(f"  URL: {img.url}")
        print(f"  position_type: {repr(img.position_type)}")
        print(f"  position_value: {repr(img.position_value)}")
        print(f"  position_mode: {repr(img.position_mode)}")
        print(f"  status: {img.status}")
        print(f"  关联产品: {[p.name for p in img.products]}")
