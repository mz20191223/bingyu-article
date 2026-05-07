import requests

BASE_URL = "http://localhost:5000/api"

login_data = {"username": "admin", "password": "123456"}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
print(f"登录响应: {response.status_code}, {response.text}")
token = response.json().get('data', {}).get('token')
headers = {"Authorization": f"Bearer {token}"}

print("\n测试获取草稿列表 (带token)...")
response = requests.get(f"{BASE_URL}/drafts", headers=headers)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:500]}")

print("\n测试不带认证...")
response = requests.get(f"{BASE_URL}/drafts")
print(f"状态码: {response.status_code}")