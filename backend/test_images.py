import sys
sys.path.insert(0, '.')

# 简化的测试脚本，直接测试图片插入逻辑
def insert_images(content, images, website_ids):
    if not images:
        return {'content': content, 'images': []}

    result_images = []
    modified_content = content

    for img in images:
        img_info = {'url': img['url'], 'position_type': img['position_type'], 'position_value': img['position_value'], 'position_mode': img['position_mode']}
        result_images.append(img_info)

        img_html = f'<p><img src="{img["url"]}" alt="产品图片" /></p>'

        if img['position_type'] == 'before_first':
            modified_content = img_html + '\n' + modified_content
        elif img['position_type'] == 'after_last':
            modified_content = modified_content + '\n' + img_html
        elif img['position_type'] == 'before_paragraph' or img['position_type'] == 'custom':
            paragraphs = modified_content.split('\n\n')
            if paragraphs == ['']:
                paragraphs = []
            pos = img['position_value'] - 1 if img['position_value'] > 0 else 0
            pos = min(pos, len(paragraphs))
            if pos < 0:
                pos = 0
            if img['position_type'] == 'before_paragraph' or img['position_mode'] == 'before':
                paragraphs.insert(pos, img_html)
            else:
                if pos + 1 <= len(paragraphs):
                    paragraphs.insert(pos + 1, img_html)
                else:
                    paragraphs.append(img_html)
            modified_content = '\n\n'.join(paragraphs)
        elif img['position_type'] == 'after_paragraph' or img['position_mode'] == 'after':
            paragraphs = modified_content.split('\n\n')
            if paragraphs == ['']:
                paragraphs = []
            pos = img['position_value'] - 1 if img['position_value'] > 0 else 0
            pos = min(pos, len(paragraphs)-1)
            if pos < 0:
                pos = 0
            if pos + 1 <= len(paragraphs):
                paragraphs.insert(pos + 1, img_html)
            else:
                paragraphs.append(img_html)
            modified_content = '\n\n'.join(paragraphs)

    return {'content': modified_content, 'images': result_images}


# 测试数据
content = '''【京东返利：为什么你需要一个靠谱的返利工具？】
在电商行业蓬勃发展的今天，京东凭借其正品保障，物流优势和品类丰富度，成为无数消费者购物的首选平台。

【高省返利APP：京东官方合作，返利更安心】
为什么说"高省返利APP"是京东返利工具中的佼佼者？

【返利力度真实透明，告别"套路优惠"】
高省返利APP坚持"真实返利、无套路"原则。'''

# 模拟图片数据
images = [
    {
        'url': 'https://example.com/image1.jpg',
        'position_type': 'before_first',
        'position_value': 1,
        'position_mode': 'before'
    },
    {
        'url': 'https://example.com/image2.jpg',
        'position_type': 'custom',
        'position_value': 2,
        'position_mode': 'after'
    }
]

print(f"原始内容:\n{content}")
print(f"\n图片数量: {len(images)}")
print(f"\n图片详情:")
for img in images:
    print(f"  URL: {img['url']}")
    print(f"  位置类型: {img['position_type']}")
    print(f"  位置值: {img['position_value']}")
    print(f"  位置模式: {img['position_mode']}")

# 测试插入图片
result = insert_images(content, images, [1])
print(f"\n插入图片后的内容:\n{result['content']}")
print(f"\n内容是否包含img标签: {'<img' in result['content']}")
