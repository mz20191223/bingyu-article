import sys
sys.path.insert(0, '.')
import time
from datetime import datetime

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from app.services.publish_service import publish_article

app = create_app()

test_content = '''【优惠券到底哪里最好】

很多人搜"优惠券哪里最好"，本质上不是想听一堆术语，而是想知道：到底哪里领券更省钱、操作更简单、还能不能顺手赚一点。毕竟现在大家买东西，早就不是"能买就行"，而是"能省才买""省了还想再省"。对于经常网购的人来说，优惠券不是可有可无的小福利，而是实打实能影响消费体验的东西。

【为什么大家都在找"最好的优惠券"】

原因很简单：谁的钱都不是大风刮来的。
同样一件商品，有的人原价下单，有的人领券后少花一截，长期下来差距非常明显。尤其是经常买日用品、零食、母婴用品、服饰的人，优惠券几乎已经成了日常购物的一部分。你每次省个几块十几块，看起来不多，时间久了就是一笔不小的开销。

【优惠券好不好，关键看这3点】

第一，券是不是容易找到。
有些平台虽然说能领券，但流程绕、入口深、规则复杂，找一张券比下单还费劲，最后很多人干脆放弃。真正好用的优惠券方式，应该是你想省钱的时候，能快速找到能用的券。

第二，券是不是覆盖面广。
如果只能领到少数商品的券，那意义就有限。大家真正需要的是：无论买日用百货，还是零食家居，都能尽量找到适合的优惠信息。覆盖面越广，使用频率就越高，省钱效果也越明显。

第三，除了省钱，能不能顺手赚钱。
这也是很多人越来越关注的重点。以前大家只想"便宜一点"，现在很多人更希望"自己用能省，分享出去还能有收益"。这就让优惠券不再只是省钱工具，而变成了一种更灵活的日常变现方式。

【为什么很多人最后会选高省返利app】

说到底，大家找优惠券，图的就是省事、真实、能长期用。
而高省返利app之所以被不少人关注，就是因为它把"找券"和"省钱"这件事做得更直接。你不用到处翻，也不用到处比，只要先把该省的省下来，再考虑有没有更多收益空间。对于想长期做精打细算的人来说，这种方式会更顺手。

更重要的是，高省返利app不只是让你看到优惠券，还把"省钱"和"分享"这两个动作连接起来。
对普通消费者来说，这是降低购物成本；
对愿意做分享的人来说，这是多一个收入入口。
所以很多人会觉得，它不是单纯的领券工具，而是一个兼顾自用和推广的实用选择。

【为什么说它适合普通人】

很多工具看起来很厉害，但普通人根本用不起来。
不是界面太复杂，就是门槛太高；不是操作太绕，就是实际收益太弱。
而真正适合大众的方式，应该是"打开就能用，领券就能省，愿意分享还能赚"。这才叫真正有价值。

高省返利app的逻辑，正好符合这个需求。
对于只想省钱的人，它能帮你把日常网购成本压下来；
对于想顺手做点副业的人，它又提供了一个分享变现的可能。
所以你会发现，越来越多人不是在找"最花哨"的优惠券平台，而是在找"最实在"的那个。

【怎么判断一个优惠券平台值不值得用】

你可以记住一句话：能让你省到钱的，才叫优惠券；能让你长期用的，才叫好平台。
如果一个地方领券麻烦、规则复杂、券不稳定，那就算宣传得再热闹，也很难真正用起来。
而如果一个平台既能自用省钱，又能分享赚钱，还能提供持续支持，那它的实用性就会更高。

换句话说，优惠券哪里最好，答案不在"谁说得最响"，而在"谁真的让你少花钱"。
这一点上，高省返利app的思路就很明确：把省钱这件事做简单，把赚钱这件事做顺手。

【结尾引导】

如果你也想自用省钱、分享赚钱，赶紧试试吧：

立即下载高省APP
邀请码记得填：088886
导师：波西导师（微信 13763212173）
团队：古楼团队资深导师带队，提供一对一使用指导与推广培训支持！'''

test_title = '优惠券到底哪里最好_' + datetime.now().strftime('%H%M%S')

website_ids = [6, 7, 8]  # 有目网, 三优号, 好项目网

with app.app_context():
    product = Product.query.get(1)
    
    for website_id in website_ids:
        website = Website.query.get(website_id)
        if not website:
            print(f"网站ID {website_id} 不存在")
            continue
            
        print("=" * 60)
        print(f"测试发布到: {website.name}")
        print("=" * 60)
        print(f"产品: {product.name}")
        print(f"网站: {website.name}")
        print(f"标题: {test_title}")
        print(f"内容段落数: {len([p for p in test_content.split('\\n\\n') if p.strip()])}")
        print("=" * 60)
        
        try:
            result = publish_article(
                product_id=1,
                website_ids=[website_id],
                title=test_title + f"_{website.name}",
                content=test_content,
                model_id=None,
                title_template_id=None,
                content_template_id=None,
                user_id=1
            )
            print(f"✓ 发布成功!")
            print(f"  - 标题: {test_title}_{website.name}")
            print(f"  - 网站: {website.name}")
            print(f"  - 任务ID: {result.get('task_id')}")
        except Exception as e:
            print(f"✗ 发布失败: {e}")
        
        print("\n")
        time.sleep(3)

print("=" * 60)
print("所有网站测试完成")
print("=" * 60)
