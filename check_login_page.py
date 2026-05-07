from playwright.sync_api import sync_playwright
import time

def check_login_page():
    website_url = "http://yomowoo.com"

    with sync_playwright() as p:
        print("启动浏览器...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(30000)

        print("访问登录页...")
        page.goto(f"{website_url}/user/sign.html")
        time.sleep(5)

        print("获取页面HTML前2000字符...")
        html = page.content()
        print(html[:2000])

        print("\n查找所有input元素...")
        inputs = page.query_selector_all("input")
        for inp in inputs:
            name = inp.get_attribute("name")
            type_attr = inp.get_attribute("type")
            id_attr = inp.get_attribute("id")
            placeholder = inp.get_attribute("placeholder")
            print(f"  name={name}, type={type_attr}, id={id_attr}, placeholder={placeholder}")

        print("\n查找所有button元素...")
        buttons = page.query_selector_all("button")
        for btn in buttons:
            text = btn.inner_text()
            type_attr = btn.get_attribute("type")
            print(f"  text={text}, type={type_attr}")

        browser.close()

if __name__ == "__main__":
    check_login_page()