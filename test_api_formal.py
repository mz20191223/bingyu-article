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
    headers = {"Authorization": f"Bearer {token}"}

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

    response = requests.post(f"{BASE_URL}/publish/submit", json=publish_data, headers=headers, timeout=300)
    return response.json()

def main():
    token = login_get_token()
    if not token:
        print("登录失败")
        return

    print("登录成功")

    title = "API正式测试_" + str(int(time.time()))
    content = "这是API正式测试的内容"

    print(f"标题: {title}")
    result = publish_article_via_api(token, title, content)
    print(f"响应: {result}")

if __name__ == "__main__":
    main()