import sys
sys.path.insert(0, '.')
import time
from datetime import datetime

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from app.services.publish_service import publish_article

app = create_app()

content = '''【每次网购都在白白多花钱，你心疼不心疼】

说实话，咱们平时网购真的没少花冤枉钱。看上一件衣服，原价199元，你直接就付款了，结果过两天发现别人只用99元就买到手，还返了十几块钱，那一刻心里真不是滋味。其实根本不是你买贵了，而是你不知道那些隐藏的优惠券在哪里领，不知道下单后还能把一部分钱拿回来。每天刷购物软件，感觉每个商品都写着"我能更便宜"，可你就是找不到那个入口，这种感觉太憋屈了。

【高省返利APP，让每一分钱都花得明明白白】

高省返利APP就是专门帮你解决这个问题的。它把所有平台商家的隐藏优惠券和返利都整合在一起，你只需要复制商品链接，打开高省，它就能自动帮你找出这张商品下面最划算的优惠券，告诉你领完券后实际付多少钱，还能再返给你一笔现金。高省的口号是"帮朋友，一起省"，没有中间商赚差价，全部佣金都直接返到你手上。不管是买衣服、买零食、买家电还是日用品，用高省先查一下再下单，那种"花小钱办大事"的快乐你试过一次就停不下来。

【用高省到底能省多少钱？算笔账你就明白了】

我给你举个真实的例子。我有个朋友想买一套护肤品，原价328元，她直接在官方店下单的话一分钱不少。但她复制链接去高省查了一下，发现有一张80元的隐藏券，领完之后商品变成248元，下单成功后还返了19块钱到她高省账户里，相当于最后只花了229元，比原价整整省了99元！这样一个月下来，光是自己家里吃的用的穿的，轻轻松松就能省出两三百块。一年就是两三千，够带全家出去短途旅游一趟了。而且高省上的返利比例非常高，很多商品能返到30%甚至50%以上，买东西不但不亏，反而感觉赚到了。

【除了省钱，还能不花钱就赚零花钱】

很多用了高省的朋友都说，最惊喜的不是自己省了多少，而是没想到还能靠它赚钱。你平时买东西觉得好用，随手分享给闺蜜或者发个朋友圈，朋友用了你的链接下单，你就能拿到一笔佣金，完全是零成本、零风险。好多宝妈、大学生、上班族下了班没事做，就把高省当副业，每天在微信群里推荐几个划算的好东西，一个月的零花钱就有着落了。而且高省完全不需要你囤货、发货、管售后，你只管分享优惠，剩下的一切都由平台和商家搞定。自用省钱是第一步，分享赚钱才是真正的快乐。

【高省怎么用？简单三步，老人小孩都能学会】

你可能会担心，这个APP会不会操作很复杂？完全不会。第一步，去应用商店搜索"高省"下载安装；第二步，打开APP注册登录；第三步也是最重要的一步：复制你想买的东西的链接，回到高省，它会自动弹出来这张商品的优惠信息，你点一下"领券购买"，就会跳转到原来的下单页面，价格已经变成了领券后的低价，而且返利也自动跟上了。买完之后，等确认收货，返利就会自动到你的高省账户里，可以随时提现到微信或者支付宝。整个过程不到十秒钟，比你去翻半天优惠券不知道快了多少倍。

【结尾引导】

如果你也想自用省钱、分享赚钱，赶紧试试吧：

立即下载高省APP
邀请码记得填：088886
导师：波西导师（微信 13763212173）
团队：古楼团队资深导师带队，提供一对一使用指导与推广培训支持！'''

test_title = '每次网购都在白白多花钱_' + datetime.now().strftime('%H%M%S')

with app.app_context():
    product = Product.query.get(1)
    website = Website.query.get(6)

    print("=" * 60)
    print("Excel内容测试 - 发布到有目网")
    print("=" * 60)
    print(f"产品: {product.name}")
    print(f"网站: {website.name}")
    print(f"标题: {test_title}")

    paragraphs = [p for p in content.split('\n\n') if p.strip()]
    print(f"内容段落数: {len(paragraphs)}")
    for i, p in enumerate(paragraphs, 1):
        preview = p[:50].replace('\n', ' ') + '...' if len(p) > 50 else p.replace('\n', ' ')
        print(f"  段落{i}: {preview}")

    print("=" * 60)

    try:
        result = publish_article(
            product_id=1,
            website_ids=[6],
            title=test_title,
            content=content,
            model_id=None,
            title_template_id=None,
            content_template_id=None,
            user_id=1
        )
        print(f"✓ 发布成功!")
        print(f"  - 标题: {test_title}")
        print(f"  - 网站: {website.name}")
        print(f"  - 任务ID: {result.get('task_id')}")
    except Exception as e:
        print(f"✗ 发布失败: {e}")
        import traceback
        traceback.print_exc()
