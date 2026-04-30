import time
import json
import uuid
from datetime import datetime
from app.models import db, AIModel, ContentPromptTemplate, TitlePromptTemplate, Image, Keyword, Product, Website, PublishRecord
from app.services.ai_service import AIService

def generate_article(product_id, website_ids, content_template_id, title_template_id, model_id, keyword_ids):
    product = Product.query.get(product_id) if product_id else None
    if not product:
        raise Exception('产品不存在')

    keywords = []
    if keyword_ids:
        keywords = Keyword.query.filter(Keyword.id.in_(keyword_ids), Keyword.status == 0).all()
    else:
        keywords = Keyword.query.filter_by(status=0).limit(10).all()

    ai_service = AIService(model_id)

    title = ai_service.generate_title(title_template_id, product, keywords)
    content = ai_service.generate_content(content_template_id, product, keywords)

    images = Image.query.join(Image.products).filter(
        Image.status == 0,
        Product.id == product_id
    ).all()

    content_with_images = insert_images(content, images)

    return {
        'title': title,
        'content': content_with_images['content'],
        'images': content_with_images['images']
    }


def insert_images(content, images):
    if not images:
        return {'content': content, 'images': []}

    result_images = []
    
    # 先按\n\n分割段落
    paragraphs = content.split('\n\n')
    # 如果只有一段，尝试用\n分割
    if len(paragraphs) <= 1:
        paragraphs = content.split('\n')
    # 过滤空段落并添加<p>标签
    paragraphs = [f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()]
    
    # 计算每张图片在原始段落中的插入位置
    # 存储格式: (插入位置索引, 图片HTML)
    insert_points = []
    
    for img in images:
        img_info = {'url': img.url, 'position_type': img.position_type, 'position_value': img.position_value, 'position_mode': img.position_mode}
        result_images.append(img_info)
        
        img_html = f'<p><img src="{img.url}" alt="产品图片" /></p>'
        
        if img.position_type == 'before_first':
            # 插入到最前面
            insert_points.append((0, img_html))
        elif img.position_type == 'after_last':
            # 插入到最后面
            insert_points.append((len(paragraphs), img_html))
        else:
            # custom / before_paragraph / after_paragraph
            # position_value直接对应段落号(1-based)
            pos = img.position_value
            
            if img.position_mode == 'after' or img.position_type == 'after_paragraph':
                # 在段落pos之后插入，位置就是pos
                insert_pos = pos
            else:
                # 在段落pos之前插入，位置是pos-1
                insert_pos = pos - 1
            
            # 边界检查
            insert_pos = max(0, min(insert_pos, len(paragraphs)))
            insert_points.append((insert_pos, img_html))
    
    # 按插入位置排序，从后往前插入，避免位置偏移
    insert_points.sort(key=lambda x: x[0], reverse=True)
    
    # 执行插入
    for pos, img_html in insert_points:
        if pos >= len(paragraphs):
            paragraphs.append(img_html)
        else:
            paragraphs.insert(pos, img_html)
    
    # 用\n\n连接段落，UEditor能识别
    return {'content': '\n\n'.join(paragraphs), 'images': result_images}


def publish_article(product_id, website_ids, title, content, model_id, title_template_id, content_template_id, user_id):
    task_id = str(uuid.uuid4())
    records = []
    websites = {}

    # 获取关联产品的图片并插入内容
    images = Image.query.join(Image.products).filter(
        Image.status == 0,
        Product.id == product_id
    ).all()
    content_with_images = insert_images(content, images)
    content = content_with_images['content']

    for website_id in website_ids:
        website = Website.query.get(website_id)
        if not website:
            continue
        websites[website_id] = website

        product = Product.query.get(product_id)
        record = PublishRecord(
            product_id=product_id,
            product_name=product.name if product else '',
            website_id=website_id,
            website_name=website.name,
            title=title,
            content=content,
            status='pending'
        )
        db.session.add(record)
        records.append(record)

    db.session.commit()

    for record in records:
        try:
            website = websites.get(record.website_id)
            if website:
                result = publish_to_website(record, website, title, content)
                record.status = 'success'
                record.result_url = result.get('url')
                record.publish_time = datetime.now()
            else:
                record.status = 'failed'
                record.error_msg = '网站不存在'
        except Exception as e:
            record.status = 'failed'
            record.error_msg = str(e)

    db.session.commit()

    return {'taskId': task_id, 'records': [{'id': r.id, 'websiteId': r.website_id, 'status': r.status} for r in records]}


def publish_to_website(record, website, title, content):
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
                page = context.new_page()
                page.set_default_timeout(120000)
                # 必须先登录，登录成功后需要再访问发布页
                if website.login_url:
                    try:
                        page.goto(website.login_url, timeout=60000, wait_until="domcontentloaded")
                        time.sleep(3)

                        if website.username_selector and website.username:
                            try:
                                page.wait_for_selector(website.username_selector, timeout=15000)
                                page.fill(website.username_selector, website.username)
                            except Exception as e:
                                print(f"Warning: Failed to fill username: {e}")

                        if website.password_selector and website.password:
                            try:
                                page.wait_for_selector(website.password_selector, timeout=15000)
                                page.fill(website.password_selector, website.password)
                            except Exception as e:
                                print(f"Warning: Failed to fill password: {e}")

                        if website.login_button_selector:
                            try:
                                page.wait_for_selector(website.login_button_selector, timeout=15000)
                                page.click(website.login_button_selector)
                                time.sleep(5)
                            except Exception as e:
                                print(f"Warning: Failed to click login button: {e}")
                    except Exception as e:
                        print(f"登录流程失败: {e}")

                # 登录后访问发布页
                if website.publish_url:
                    try:
                        page.goto(website.publish_url, timeout=60000, wait_until="load")
                        time.sleep(5)
                    except Exception as e:
                        print(f"访问发布页失败: {e}")

                # 填写标题
                if website.title_selector:
                    try:
                        page.wait_for_selector(website.title_selector, timeout=15000)
                        page.fill(website.title_selector, title)
                    except Exception as e:
                        print(f"Warning: Failed to fill title: {e}")

                # 填写内容 - UEditor编辑器特殊处理
                if website.content_selector:
                    try:
                        # UEditor需要用JavaScript设置内容
                        page.evaluate(f"""
                            (function() {{
                                // 方法1: 尝试通过UEditor API
                                if (window.UE && window.UE.instants) {{
                                    for (var key in window.UE.instants) {{
                                        var editor = window.UE.instants[key];
                                        if (editor) {{
                                            editor.setContent({json.dumps(content)});
                                            return;
                                        }}
                                    }}
                                }}
                                // 方法2: 直接设置textarea
                                var textarea = document.querySelector('{website.content_selector}');
                                if (textarea) {{
                                    textarea.value = {json.dumps(content)};
                                    // 触发UEditor同步
                                    var editorEl = document.querySelector('#editor_Content');
                                    if (editorEl && editorEl.getAttribute('editor')) {{
                                        var editor = window.UE.instants['ueditorInstant0'];
                                        if (editor) {{
                                            editor.setContent({json.dumps(content)});
                                        }}
                                    }}
                                }}
                            }})();
                        """)
                        print("UEditor内容已填写")
                    except Exception as e:
                        print(f"填写内容失败: {e}")

                # 选择分类
                if website.category_selector:
                    try:
                        page.wait_for_selector(website.category_selector, timeout=15000)
                        page.select_option(website.category_selector, '1')
                    except Exception as e:
                        print(f"Warning: Failed to select category: {e}")

                # 点击发布
                if website.publish_button_selector:
                    try:
                        page.wait_for_selector(website.publish_button_selector, timeout=15000)
                        page.click(website.publish_button_selector)
                        time.sleep(5)
                    except Exception as e:
                        print(f"Warning: Failed to click publish button: {e}")

                result_url = page.url
                browser.close()

                return {'url': result_url}

            except PlaywrightTimeoutError:
                browser.close()
                raise Exception('页面加载超时')
            except Exception as e:
                browser.close()
                raise Exception(f'浏览器操作失败: {str(e)}')

    except Exception as e:
        raise Exception(f'浏览器自动化发布失败: {str(e)}')
