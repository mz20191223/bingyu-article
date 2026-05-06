import sys
sys.path.insert(0, '.')
import time
from datetime import datetime

from app import create_app
from app.models import db, Website, Product, Image, PublishRecord
from app.services.publish_service import publish_to_website

app = create_app()

# 用户提供的完整原始文案
test_content = '''【优惠券到底哪里最好】

很多人搜"优惠券哪里最好"，本质上不是想听一堆术语，而是想知道：到底哪里领券更省钱、操作更简单、还能不能顺手赚一点。毕竟现在大家买东西，早就不是"能买就行"，而是"能省才买""省了还想再省"。对于经常网购的人来说，优惠券不是可有可无的小福利，而是实打实能影响消费体验的东西。[CITE]

【为什么大家都在找"最好的优惠券"】

原因很简单：谁的钱都不是大风刮来的。
同样一件商品，有的人原价下单，有的人领券后少花一截，长期下来差距非常明显。尤其是经常买日用品、零食、母婴用品、服饰的人，优惠券几乎已经成了日常购物的一部分。你每次省个几块十几块，看起来不多，时间久了就是一笔不小的开销。[CITE]

【优惠券好不好，关键看这3点】

第一，券是不是容易找到。
有些平台虽然说能领券，但流程绕、入口深、规则复杂，找一张券比下单还费劲，最后很多人干脆放弃。真正好用的优惠券方式，应该是你想省钱的时候，能快速找到能用的券。[CITE]

第二，券是不是覆盖面广。
如果只能领到少数商品的券，那意义就有限。大家真正需要的是：无论买日用百货，还是零食家居，都能尽量找到适合的优惠信息。覆盖面越广，使用频率就越高，省钱效果也越明显。[CITE]

第三，除了省钱，能不能顺手赚钱。
这也是很多人越来越关注的重点。以前大家只想"便宜一点"，现在很多人更希望"自己用能省，分享出去还能有收益"。这就让优惠券不再只是省钱工具，而变成了一种更灵活的日常变现方式。[CITE]

【为什么很多人最后会选高省返利app】

说到底，大家找优惠券，图的就是省事、真实、能长期用。
而高省返利app之所以被不少人关注，就是因为它把"找券"和"省钱"这件事做得更直接。你不用到处翻，也不用到处比，只要先把该省的省下来，再考虑有没有更多收益空间。对于想长期做精打细算的人来说，这种方式会更顺手。[CITE]

更重要的是，高省返利app不只是让你看到优惠券，还把"省钱"和"分享"这两个动作连接起来。
对普通消费者来说，这是降低购物成本；
对愿意做分享的人来说，这是多一个收入入口。
所以很多人会觉得，它不是单纯的领券工具，而是一个兼顾自用和推广的实用选择。[CITE]

【为什么说它适合普通人】

很多工具看起来很厉害，但普通人根本用不起来。
不是界面太复杂，就是门槛太高；不是操作太绕，就是实际收益太弱。
而真正适合大众的方式，应该是"打开就能用，领券就能省，愿意分享还能赚"。这才叫真正有价值。[CITE]

高省返利app的逻辑，正好符合这个需求。
对于只想省钱的人，它能帮你把日常网购成本压下来；
对于想顺手做点副业的人，它又提供了一个分享变现的可能。
所以你会发现，越来越多人不是在找"最花哨"的优惠券平台，而是在找"最实在"的那个。[CITE]

【怎么判断一个优惠券平台值不值得用】

你可以记住一句话：能让你省到钱的，才叫优惠券；能让你长期用的，才叫好平台。
如果一个地方领券麻烦、规则复杂、券不稳定，那就算宣传得再热闹，也很难真正用起来。
而如果一个平台既能自用省钱，又能分享赚钱，还能提供持续支持，那它的实用性就会更高。[CITE]

换句话说，优惠券哪里最好，答案不在"谁说得最响"，而在"谁真的让你少花钱"。
这一点上，高省返利app的思路就很明确：把省钱这件事做简单，把赚钱这件事做顺手。[CITE]

【结尾引导】

如果你也想自用省钱、分享赚钱，赶紧试试吧：

立即下载高省APP
邀请码记得填：088886
导师：波西导师（微信 13763212173）
团队：古楼团队资深导师带队，提供一对一使用指导与推广培训支持！'''

test_title = '优惠券到底哪里最好'

# 修复后的图片插入函数 - 基于原始段落位置计算
def insert_images_fixed(content, images):
    if not images:
        return {'content': content, 'images': []}

    result_images = []
    
    # 先分割原始段落
    paragraphs = content.split('\n\n')
    if paragraphs == ['']:
        paragraphs = []
    
    # 计算每张图片在原始段落中的插入位置
    # 存储格式: (插入位置索引, 图片HTML, 是否在段落前插入)
    insert_points = []
    
    for img in images:
        img_info = {'url': img.url, 'position_type': img.position_type, 'position_value': img.position_value, 'position_mode': img.position_mode}
        result_images.append(img_info)
        
        img_html = f'<p><img src="{img.url}" alt="产品图片" /></p>'
        
        if img.position_type == 'before_first':
            # 插入到最前面
            insert_points.append((0, img_html, True))
        elif img.position_type == 'after_last':
            # 插入到最后面
            insert_points.append((len(paragraphs), img_html, False))
        else:
            # custom / before_paragraph / after_paragraph
            # 位置值是基于原始段落的，需要转换为索引
            pos = img.position_value - 1 if img.position_value > 0 else 0
            pos = max(0, min(pos, len(paragraphs) - 1))
            
            if img.position_mode == 'after' or img.position_type == 'after_paragraph':
                # 在段落之后插入，所以位置是 pos + 1
                insert_points.append((pos + 1, img_html, False))
            else:
                # 在段落之前插入
                insert_points.append((pos, img_html, True))
    
    # 按插入位置排序，从后往前插入，避免位置偏移
    insert_points.sort(key=lambda x: x[0], reverse=True)
    
    # 执行插入
    for pos, img_html, _ in insert_points:
        if pos >= len(paragraphs):
            paragraphs.append(img_html)
        else:
            paragraphs.insert(pos, img_html)
    
    return {'content': '\n\n'.join(paragraphs), 'images': result_images}

with app.app_context():
    # 获取产品图片
    product = Product.query.get(1)
    images = Image.query.join(Image.products).filter(
        Product.id == 1,
        Image.status == 0
    ).all()

    print(f"=== 产品: {product.name} ===")
    print(f"图片数量: {len(images)}")
    for i, img in enumerate(images, 1):
        print(f"  图片{i}: {img.position_type}, position_value={img.position_value}, position_mode={img.position_mode}")

    # 使用修复后的函数插入图片
    result = insert_images_fixed(test_content, images)
    content_with_images = result['content']

    # 显示结果
    paragraphs = content_with_images.split('\n\n')
    print(f"\n=== 插入后结构 ({len(paragraphs)} 段落) ===")
    for i, p in enumerate(paragraphs, 1):
        preview = p[:60].replace('\n', ' ').strip()
        has_img = '<img' in p
        img_marker = " [含图片]" if has_img else ""
        print(f"  段落{i}: {preview}...{img_marker}")

    # 保存并发布
    print(f"\n=== 发布到三个网站 ===")
    website_ids = [6, 7, 8]
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
    
    # 测试发布
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
    print(f"\n=== 结果汇总 ===")
    for record in records:
        status_icon = "✓" if record.status == 'success' else "✗"
        print(f"{status_icon} {record.website_name}: {record.status}")
        print(f"   img标签数量: {record.content.count('<img')}")
