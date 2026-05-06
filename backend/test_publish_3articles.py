import sys
sys.path.insert(0, '.')
import time
from datetime import datetime

from app import create_app
from app.models import db, Website, Product, Image
from app.services.publish_service import publish_article

app = create_app()

test_content = '''你是不是也经常买完东西就后悔

说实话，咱们平时网购真的踩过太多坑了。看上一件衣服179元，觉得价格还行就直接付款了，结果过两天发现别人只花了89元就买到手，还返了十几块现金。你说气不气人？不是东西贵，而是你根本不知道那些藏在角落里的隐藏优惠券在哪领，也不知道下单之后还能把钱拿回来一部分。每天刷购物软件，感觉每个商品都在跟你说"我能更便宜"，可你就是找不到那个省钱的门路，这种感觉真的太憋屈了。

高省返利APP到底是个什么神仙工具

高省返利APP就是专门帮你解决这个痛点的。它的口号特别真诚——"帮朋友，一起省"，把所有网购平台的优惠券和返利都整合到一起，没有任何中间商赚差价，全部佣金直接返到你手上。不管你买衣服、零食、家电还是日用品，只要复制商品链接，打开高省，它就能自动帮你找出这张商品下面最划算的隐藏优惠券，告诉你领完券后实付多少钱，还能额外返一笔现金到你的账户。用高省先查再下单，那种"花小钱办大事"的快乐，你试过一次就再也离不开了。

算一笔账，用高省一年能省下多少钱

我给你说个真实的例子。我一个朋友想买一套品牌护肤品，原价328元，如果直接在官方店下单，一分钱都少不了。但她复制链接去高省查了一下，发现有一张80元的隐藏券，领完之后商品变成248元，下单成功后又返了19块钱到高省账户里，最后相当于只花了229元，比原价整整省了99元！这样一个月下来，光是家里吃的用的穿的，轻轻松松就能省出两三百块。一年就是两三千，够全家出去短途旅游一趟了。而且高省上的返利比例普遍很高，很多商品能返到30%甚至50%以上，买东西不但不亏，反而感觉像是在赚钱。

结尾引导

如果你也想自用省钱、分享赚钱，赶紧试试吧：

立即下载高省APP
邀请码记得填：088886
导师：波西导师（微信 13763212173）
团队：古楼团队资深导师带队，提供一对一使用指导与推广培训支持！'''

test_title = '你是不是也经常买完东西就后悔_' + datetime.now().strftime('%H%M%S')

with app.app_context():
    product = Product.query.filter_by(status=0).first()
    websites = Website.query.filter_by(status=0).limit(3).all()

    print(f"产品: {product.name if product else 'None'}")
    print(f"网站数量: {len(websites)}")
    for w in websites:
        print(f"  - {w.name} (ID: {w.id})")

    if not product or len(websites) < 3:
        print("错误: 没有足够的产品或网站")
        exit(1)

    print("\n开始发布测试...\n")

    for i, website in enumerate(websites, 1):
        print("=" * 60)
        print(f"第 {i} 篇发布到: {website.name}")
        print("=" * 60)

        title = test_title + f"_{website.name}"
        paragraphs = [p for p in test_content.split('\n\n') if p.strip()]
        print(f"标题: {title}")
        print(f"内容段落数: {len(paragraphs)}")
        print(f"内容长度: {len(test_content)} 字符")

        try:
            result = publish_article(
                product_id=product.id,
                website_ids=[website.id],
                title=title,
                content=test_content,
                model_id=None,
                title_template_id=None,
                content_template_id=None,
                user_id=1
            )
            print(f"✓ 第 {i} 篇发布成功!")
            print(f"  - 任务ID: {result.get('task_id')}")
        except Exception as e:
            print(f"✗ 第 {i} 篇发布失败: {e}")

        print()
        if i < 3:
            print("等待3秒...")
            time.sleep(3)

    print("=" * 60)
    print("测试完成，请检查目标网站文章是否正常")
    print("=" * 60)
