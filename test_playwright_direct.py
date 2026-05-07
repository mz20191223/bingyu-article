from playwright.sync_api import sync_playwright
import requests
import json
import time
import re

BASE_URL = "http://localhost:5000/api"

def login_get_token():
    """登录获取token"""
    login_data = {"username": "admin", "password": "123456"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('token')
    return None

def generate_content(token, product_id, keywords):
    """调用AI生成标题和内容"""
    headers = {"Authorization": f"Bearer {token}"}

    generate_data = {
        "productId": product_id,
        "keywordIds": [],
        "keywords": keywords,
        "modelId": None
    }

    print(f"正在调用AI生成内容，关键词: {keywords}")
    response = requests.post(f"{BASE_URL}/ai/generate", json=generate_data, headers=headers)
    print(f"AI生成响应状态: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 200:
            data = result.get('data', {})
            title = data.get('title', '')
            content = data.get('content', '')
            print(f"AI生成成功！")
            print(f"标题: {title}")
            print(f"内容长度: {len(content)}")
            return title, content

    print(f"AI生成失败: {response.text}")
    return None, None

def find_article_by_title(page, title):
    """根据标题查找文章并进入详情页获取链接"""
    time.sleep(3)

    clean_title = re.sub(r'[【】\[\]（）\(\)]', '', title).strip()
    print(f"\n===== 查找文章标题: {clean_title} =====")

    try:
        all_links = page.query_selector_all('a[href]')
        print(f"页面上找到 {len(all_links)} 个链接")

        for link in all_links:
            href = link.get_attribute('href')
            if not href:
                continue

            # 跳过不是文章链接的URL
            if not (('/post/' in href or '/article/' in href or '/info/' in href or '.html' in href)):
                continue

            try:
                link_text = link.inner_text().strip()
            except:
                link_text = ""

            link_text_clean = re.sub(r'[【】\[\]（）\(\)]', '', link_text).strip()

            # 多种匹配方式
            matched = False
            if clean_title and link_text_clean:
                # 精确匹配
                if link_text_clean == clean_title:
                    matched = True
                    print(f"精确匹配成功!")
                # 包含匹配（标题在链接文本中）
                elif clean_title in link_text_clean:
                    matched = True
                    print(f"包含匹配成功!")
                # 前15个字符匹配（处理标题被截断的情况）
                elif len(clean_title) > 10 and link_text_clean.startswith(clean_title[:15]):
                    matched = True
                    print(f"前缀匹配成功!")

            if matched:
                print(f"找到文章链接: {href}")
                print(f"匹配的标题文本: {link_text_clean}")
                link.click()
                time.sleep(5)
                detail_url = page.url
                print(f"详情页URL: {detail_url}")

                return detail_url

        print("精确匹配未找到，尝试只根据URL模式查找...")
        # 如果没有找到标题匹配的链接，尝试找最新的文章链接
        article_links = []
        for link in all_links:
            href = link.get_attribute('href')
            if href and ('/post/' in href or '/article/' in href or '/info/' in href):
                # 排除包含 "comment" 或 "reply" 的链接
                if 'comment' not in href.lower() and 'reply' not in href.lower():
                    article_links.append(href)

        if article_links:
            # 取第一个文章链接作为结果（最新发布的通常在前面）
            print(f"找到 {len(article_links)} 个文章链接，使用第一个")
            first_link = article_links[0]
            print(f"文章链接: {first_link}")

            # 尝试点击进入详情页
            for link in all_links:
                href = link.get_attribute('href')
                if href == first_link:
                    link.click()
                    time.sleep(5)
                    return page.url

            return first_link

        print("未找到文章链接")

    except Exception as e:
        print(f"查找文章失败: {e}")
        import traceback
        traceback.print_exc()

    # 返回当前页面URL作为默认值
    return page.url

def publish_with_playwright(title, content):
    """使用Playwright直接发布文章"""
    website_url = "https://yomowoo.com"
    username = "290191683@qq.com"
    password = "a12345678"

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.set_default_timeout(60000)

            # 1. 登录
            print("\n===== 开始登录 =====")
            page.goto(f"{website_url}/user/sign.html", timeout=60000)
            time.sleep(3)

            page.fill("input[name='email']", username)
            page.fill("input[name='password']", password)
            page.click("button[type='submit']")
            time.sleep(5)
            print("登录完成")

            # 2. 访问发布页
            print("\n===== 访问发布页 =====")
            page.goto(f"{website_url}/user/postedt.html", timeout=60000)
            time.sleep(5)

            # 3. 填写标题
            print("\n===== 填写标题 =====")
            page.fill("input[name='title']", title)
            print(f"标题已填写: {title}")

            # 4. 填写内容 - UEditor编辑器特殊处理
            print("\n===== 填写内容 =====")
            page.evaluate(f"""
                (function() {{
                    if (window.UE && window.UE.instants) {{
                        for (var key in window.UE.instants) {{
                            var editor = window.UE.instants[key];
                            if (editor) {{
                                editor.setContent({json.dumps(content)});
                                return;
                            }}
                        }}
                    }}
                    var textarea = document.querySelector('textarea[name="content"]');
                    if (textarea) {{
                        textarea.value = {json.dumps(content)};
                    }}
                }})();
            """)
            print("内容已填写")
            time.sleep(2)

            # 5. 选择分类
            print("\n===== 选择分类 =====")
            try:
                page.select_option("select[name='category_id']", '1')
                print("分类已选择")
            except Exception as e:
                print(f"选择分类失败: {e}")

            # 6. 点击发布
            print("\n===== 点击发布 =====")
            page.click("button.submit")
            time.sleep(8)
            print("发布完成，等待跳转...")

            # 7. 跳转到文章列表页
            print("\n===== 跳转到文章列表页 =====")
            postlist_url = f"{website_url}/user/postlist.html"
            page.goto(postlist_url, timeout=60000)
            time.sleep(5)
            print(f"已访问: {page.url}")

            # 8. 查找文章
            article_url = find_article_by_title(page, title)
            print(f"\n===== 最终文章链接: {article_url} =====")

            browser.close()
            return article_url

        except Exception as e:
            print(f"浏览器操作失败: {e}")
            import traceback
            traceback.print_exc()
            browser.close()
            return None

def get_random_keyword(token):
    """随机获取一个关键词"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/keywords?page=1&size=100", headers=headers)
    if response.status_code == 200:
        result = response.json()
        keywords = result.get('data', {}).get('list', [])
        if keywords:
            import random
            keyword = random.choice(keywords)
            return keyword.get('keyword')  # 字段名是 keyword 不是 name
    return "高省返利APP"

def main():
    print("=" * 60)
    print("开始测试文章发布流程 (直接使用Playwright)")
    print("=" * 60)

    # 1. 登录获取token
    token = login_get_token()
    if not token:
        print("登录失败!")
        return

    print(f"登录成功!\n")

    # 2. 获取产品和网站信息
    headers = {"Authorization": f"Bearer {token}"}

    # 获取网站
    response = requests.get(f"{BASE_URL}/websites", headers=headers)
    websites = response.json().get('data', {}).get('list', [])
    if not websites:
        print("没有找到网站")
        return
    website = websites[0]
    print(f"使用网站: {website.get('name')} (ID: {website.get('id')})")

    # 获取产品
    response = requests.get(f"{BASE_URL}/products", headers=headers)
    products = response.json().get('data', {}).get('list', [])
    if not products:
        print("没有找到产品")
        return
    product = products[0]
    print(f"使用产品: {product.get('name')} (ID: {product.get('id')})\n")

    # 3. 随机获取关键词
    keyword = get_random_keyword(token)
    print(f"随机获取关键词: {keyword}")

    # 4. 调用AI生成标题和内容
    title, content = generate_content(token, product.get('id'), keyword)
    if not title or not content:
        print("AI生成失败，测试终止")
        return

    # 4. 使用Playwright直接发布
    print("\n" + "=" * 60)
    print("开始使用Playwright发布文章")
    print("=" * 60)
    article_url = publish_with_playwright(title, content)

    print("\n" + "=" * 60)
    print(f"测试完成! 文章链接: {article_url}")
    print("=" * 60)

    # 5. 验证链接格式
    if article_url and "/post/" in article_url and ".html" in article_url:
        print("✅ 文章链接格式正确!")
    else:
        print(f"❌ 文章链接格式不正确: {article_url}")

if __name__ == "__main__":
    main()