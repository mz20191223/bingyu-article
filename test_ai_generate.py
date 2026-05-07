import requests

BASE_URL = "http://localhost:5000/api"

def login_get_token():
    login_data = {"username": "admin", "password": "123456"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json().get('data', {}).get('token')
    return None

def generate_content(token, product_id, keywords):
    headers = {"Authorization": f"Bearer {token}"}
    generate_data = {
        "productId": product_id,
        "keywordIds": [],
        "keywords": keywords,
        "modelId": None
    }
    print(f"请求数据: {generate_data}")
    response = requests.post(f"{BASE_URL}/ai/generate", json=generate_data, headers=headers, timeout=120)
    print(f"响应状态: {response.status_code}")
    print(f"响应内容: {response.text}")
    return None, None

def main():
    token = login_get_token()
    if not token:
        print("登录失败")
        return

    print("登录成功")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/products", headers=headers)
    products = response.json().get('data', {}).get('list', [])
    product = products[0]
    print(f"使用产品: {product.get('name')}, ID: {product.get('id')}")

    generate_content(token, product.get('id'), "高省返利APP")

if __name__ == "__main__":
    main()