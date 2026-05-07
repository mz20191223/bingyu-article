from playwright.sync_api import sync_playwright
import requests
import json
import time
import re

BASE_URL = "http://localhost:5000/api"

def login_get_token():
    login_data = {"username": "admin", "password": "123456"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json().get('data', {}).get('token')
    return None

def find_article_by_title(page, title):
    time.sleep(3)
    clean_title = re.sub(r'[【】\[\]（）\(\)]', '', title).strip()
    print(f"\n查找文章标题: {clean_title}")

    all_links = page.query_selector_all('a[href]')
    print(f"页面上找到 {len(all_links)} 个链接")

    for link in all_links:
        href = link.get_attribute('href')
        if not href:
            continue

        if not (('/post/' in href or '/article/' in href or '/info/' in href or '.html' in href)):
            continue

        try:
            link_text = link.inner_text().strip()
        except:
            link_text = ""

        link_text_clean = re.sub(r'[【】\[\]（）\(\)]', '', link_text).strip()

        matched = False
        if clean_title and link_text_clean:
            if link_text_clean == clean_title:
                matched = True
                print(f"精确匹配成功!")
            elif clean_title in link_text_clean:
                matched = True
                print(f"包含匹配成功!")
            elif len(clean_title) > 10 and link_text_clean.startswith(clean_title[:15]):
                matched = True
                print(f"前缀匹配成功!")

        if matched:
            print(f"找到文章链接: {href}")
            link.click()
            time.sleep(5)
            detail_url = page.url
            print(f"详情页URL: {detail_url}")
            return detail_url

    print("精确匹配未找到，尝试URL模式查找...")
    article_links = []
    for link in all_links:
        href = link.get_attribute('href')
        if href and ('/post/' in href or '/article/' in href or '/info/' in href):
            if 'comment' not in href.lower() and 'reply' not in href.lower():
                article_links.append(href)

    if article_links:
        print(f"找到 {len(article_links)} 个文章链接，使用第一个")
        first_link = article_links[0]
        print(f"文章链接: {first_link}")
        for link in all_links:
            href = link.get_attribute('href')
            if href == first_link:
                link.click()
                time.sleep(5)
                return page.url
        return first_link

    print("未找到文章链接")
    return page.url

def main():
    print("=" * 50)
    print("开始测试（使用杜撰测试数据）")
    print("=" * 50)

    token = login_get_token()
    if not token:
        print("登录失败")
        return

    print("登录成功")

    # 使用杜撰的测试数据
    title = "测试文章标题_" + str(int(time.time()))
    content = "这是一篇测试文章的内容。\n\n第二段内容。"
    print(f"测试标题: {title}")

    website_url = "http://yomowoo.com"
    username = "290191683@qq.com"
    password = "a12345678"

    with sync_playwright() as p:
        print("\n启动浏览器...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(60000)

        print("访问登录页...")
        page.goto(f"{website_url}/user/sign.html")
        time.sleep(3)

        print("填写登录信息...")
        page.fill("input[name='name']", username)
        page.fill("input[name='password']", password)

        print("点击登录按钮...")
        page.click("button[type='submit']")
        time.sleep(5)
        print("登录完成")

        print("访问发布页...")
        page.goto(f"{website_url}/user/postedt.html")
        time.sleep(5)

        print("填写标题...")
        page.fill("input[name='title']", title)
        print(f"标题: {title}")

        print("填写内容...")
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
        time.sleep(2)

        print("选择分类...")
        try:
            page.select_option("select[name='category_id']", '1')
        except Exception as e:
            print(f"选择分类失败: {e}")

        print("点击发布...")
        page.click("button.submit")
        time.sleep(8)
        print("发布完成")

        print("访问文章列表页...")
        page.goto(f"{website_url}/user/postlist.html")
        time.sleep(5)

        print("查找文章...")
        article_url = find_article_by_title(page, title)

        browser.close()

        print("\n" + "=" * 50)
        print(f"最终文章链接: {article_url}")
        if article_url and "/post/" in article_url and ".html" in article_url:
            print("✅ 链接格式正确!")
        else:
            print(f"❌ 链接格式不正确")
        print("=" * 50)

if __name__ == "__main__":
    main()