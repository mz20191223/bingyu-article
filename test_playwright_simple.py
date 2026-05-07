from playwright.sync_api import sync_playwright
import time

def test_basic():
    """测试Playwright基本功能"""
    print("开始测试Playwright基本功能...")
    with sync_playwright() as p:
        print("启动浏览器...")
        browser = p.chromium.launch(headless=True)
        print("创建页面...")
        page = browser.new_page()
        print("访问网站...")
        page.goto("https://www.baidu.com", timeout=30000)
        print(f"页面标题: {page.title()}")
        print("关闭浏览器...")
        browser.close()
        print("测试完成!")

if __name__ == "__main__":
    test_basic()