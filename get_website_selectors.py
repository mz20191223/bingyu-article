from playwright.sync_api import sync_playwright
import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def login_get_token():
    login_data = {"username": "admin", "password": "123456"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json().get('data', {}).get('token')
    return None

def get_website_config(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/websites", headers=headers)
    if response.status_code == 200:
        websites = response.json().get('data', {}).get('list', [])
        if websites:
            return websites[0]
    return None

def main():
    token = login_get_token()
    if not token:
        print("登录失败")
        return

    website = get_website_config(token)
    if not website:
        print("获取网站配置失败")
        return

    print("网站配置信息:")
    print(f"  名称: {website.get('name')}")
    print(f"  登录URL: {website.get('login_url')}")
    print(f"  发布URL: {website.get('publish_url')}")
    print(f"  用户名选择器: {website.get('username_selector')}")
    print(f"  密码选择器: {website.get('password_selector')}")
    print(f"  登录按钮选择器: {website.get('login_button_selector')}")
    print(f"  标题选择器: {website.get('title_selector')}")
    print(f"  内容选择器: {website.get('content_selector')}")
    print(f"  分类选择器: {website.get('category_selector')}")
    print(f"  发布按钮选择器: {website.get('publish_button_selector')}")

if __name__ == "__main__":
    main()