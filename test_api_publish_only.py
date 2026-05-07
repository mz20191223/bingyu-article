import requests
import time

BASE_URL = "http://localhost:5000/api"

def login_get_token():
    login_data = {"username": "admin", "password": "123456"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json().get('data', {}).get('token')
    return None

def publish_article_via_api(token, title, content):
    """通过后端API发布文章"""
    headers = {"Authorization": f"Bearer {token}"}

    # 获取网站和产品
    response = requests.get(f"{BASE_URL}/websites", headers=headers)
    websites = response.json().get('data', {}).get('list', [])
    website = websites[0]

    response = requests.get(f"{BASE_URL}/products", headers=headers)
    products = response.json().get('data', {}).get('list', [])
    product = products[0]

    publish_data = {
        "title": title,
        "content": content,
        "productId": product.get('id'),
        "websiteIds": [website.get('id')]
    }

    print(f"调用发布API...")
    print(f"标题: {title}")
    response = requests.post(f"{BASE_URL}/publish/submit", json=publish_data, headers=headers, timeout=300)
    print(f"发布响应状态: {response.status_code}")
    print(f"发布响应内容: {response.text}")
    return response.json()

def main():
    print("=" * 50)
    print("通过后端API测试发布")
    print("=" * 50)

    token = login_get_token()
    if not token:
        print("登录失败")
        return

    print("登录成功")

    # 使用杜撰的测试数据
    title = "测试文章API发布_" + str(int(time.time()))
    content = "这是一篇通过API发布的测试文章内容。"

    result = publish_article_via_api(token, title, content)

    print("\n" + "=" * 50)
    if result.get('code') == 200:
        records = result.get('data', {}).get('records', [])
        if records:
            record = records[0]
            print(f"发布记录ID: {record.get('id')}")
            print(f"发布状态: {record.get('status')}")
    print("=" * 50)

if __name__ == "__main__":
    main()