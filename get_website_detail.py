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

def get_website_detail(token, website_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/websites/{website_id}", headers=headers)
    if response.status_code == 200:
        return response.json().get('data')
    return None

def main():
    token = login_get_token()
    if not token:
        print("登录失败")
        return

    # 获取网站详情（ID=6 有目网）
    website = get_website_detail(token, 6)
    if website:
        print("有目网完整配置信息:")
        for key, value in website.items():
            print(f"  {key}: {value}")
    else:
        print("获取网站详情失败")

if __name__ == "__main__":
    main()