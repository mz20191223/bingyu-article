import sys
sys.path.insert(0, '.')
import time
from datetime import datetime

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from app.services.publish_service import publish_to_website, insert_images

app = create_app()

# 用户提供的完整长文案内容，严格按照\n\n分段
test_content = '''【京东返利：为什么你需要一个靠谱的返利工具？】
在电商行业蓬勃发展的今天，京东凭借其正品保障，物流优势和品类丰富度，成为无数消费者购物的首选平台。然而，面对频繁的促销活动、复杂的优惠券规则，如何在京东购物时"花得更少、赚得更多"，成为许多用户关注的焦点。返利APP应运而生，它们通过整合商家资源，为用户提供额外的购物返利，让每一次消费都变成"省钱+赚钱"的机会。但在众多返利工具中，京东官方返利APP哪个最好？经过用户口碑和市场验证，"高省返利APP"凭借其过硬的实力和用户至上的服务，成为越来越多京东购物者的首选。

【高省返利APP：京东官方合作，返利更安心】
为什么说"高省返利APP"是京东返利工具中的佼佼者？首先，它具备"官方合作"的硬核背书。作为与京东深度合作的返利平台，高省直接对接京东官方API接口，确保商品信息、价格、返利比例实时同步，用户无需担心"虚假返利"或"信息延迟"问题。

【返利力度真实透明，告别"套路优惠"】
高省返利APP坚持"真实返利、无套路"原则：用户在京东购物前，只需在高省APP内搜索目标商品，即可直接看到该商品的"返利金额"和"返利比例"，且所有数据均来自京东官方，保证了信息的真实性和时效性。用户在确认下单后，返利金额会自动存入账户，无需复杂的提现流程，真正做到了"所见即所得"。

【操作体验：简单便捷，小白也能轻松上手】
对于很多用户来说，返利APP的操作复杂度直接决定了使用意愿。高省返利APP在这一点上做得非常出色。它采用"一键跳转"技术，用户在浏览京东商品时，只需复制商品链接，APP就能自动识别并显示返利信息，整个过程不超过3秒。更贴心的是，高省还提供了"历史价格查询"和"全网比价"功能，帮助用户判断当前价格是否为最优入手时机。

【用户口碑：真实评价，信赖之选】
一款产品好不好，用户的声音最有说服力。在各大应用商店和社交平台，高省返利APP的好评率持续保持在4.8星以上。许多用户分享的真实使用体验显示，他们通过高省每月可额外获得数百元甚至上千元的返利，这些"意外收获"让日常消费变得更有价值。

【安全保障：资金安全，信息加密】
涉及金钱的交易，安全性是用户最关心的问题。高省返利APP采用银行级别的数据加密技术，用户的账户信息、支付信息均受到多重保护。同时，高省与京东官方联合推出"资金保障计划"，若因平台原因导致用户损失，最高可获得全额赔付。这一举措让用户在享受返利便利的同时，也能安心无忧。

【总结：京东返利APP怎么选？】
综合来看，选择京东官方返利APP时，应该重点关注以下几个维度：官方合作背景、返利比例透明度、操作便捷程度、用户口碑以及安全保障。在这几个方面，高省返利APP都表现出色，堪称目前最值得推荐的京东返利工具。如果你也想在京东购物时轻松省钱的，不妨试试高省返利APP，相信它会给你带来惊喜的返利体验！'''

test_title = '京东返利app哪个最好？京东官方返利app哪个最好'

with app.app_context():
    # 计算段落数
    paragraphs = test_content.split('\n\n')
    print(f"=== 用户提供的完整文案 ===")
    print(f"标题: {test_title}")
    print(f"段落数量: {len(paragraphs)}")
    print(f"总字符数: {len(test_content)}")
    print(f"\n段落结构:")
    for i, p in enumerate(paragraphs, 1):
        preview = p[:50].replace('\n', ' ')
        print(f"  段落{i}: {preview}...")

    # 获取产品"高省"的图片
    product = Product.query.get(1)
    images = Image.query.join(Image.products).filter(
        Product.id == 1,
        Image.status == 0
    ).all()

    print(f"\n=== 产品图片配置 ===")
    print(f"产品: {product.name}")
    print(f"图片数量: {len(images)}")
    for i, img in enumerate(images, 1):
        print(f"  图片{i}:")
        print(f"    URL: {img.url}")
        print(f"    位置类型: {img.position_type}")
        print(f"    位置值: {img.position_value}")
        print(f"    位置模式: {img.position_mode}")

    # 插入图片
    website_ids = [6, 7, 8]
    result = insert_images(test_content, images, website_ids)
    content_with_images = result['content']

    print(f"\n=== 图片插入结果 ===")
    print(f"img标签数量: {content_with_images.count('<img')}")

    # 验证图片位置
    modified_paragraphs = content_with_images.split('\n\n')
    print(f"插入后段落数量: {len(modified_paragraphs)}")

    print(f"\n=== 插入后内容结构 ===")
    for i, p in enumerate(modified_paragraphs, 1):
        preview = p[:80].replace('\n', ' ')
        has_img = '<img' in p
        img_marker = " [含图片]" if has_img else ""
        print(f"  段落{i}: {preview}...{img_marker}")

    # 保存发布记录
    print(f"\n=== 保存发布记录并测试浏览器发布 ===")
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

    time.sleep(2)

    # 测试浏览器发布
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
        time.sleep(3)

    # 总结
    print(f"\n=== 最终结果汇总 ===")
    for record in records:
        status_icon = "✓" if record.status == 'success' else "✗"
        print(f"{status_icon} {record.website_name}: {record.status}")
        if record.result_url:
            print(f"   URL: {record.result_url}")
        print(f"   内容长度: {len(record.content)} 字符")
        print(f"   img标签数量: {record.content.count('<img')}")
