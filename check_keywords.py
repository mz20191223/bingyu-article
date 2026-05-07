import requests

BASE_URL = "http://localhost:5000/api"

def login_get_token():
    login_data = {"username": "admin", "password": "123456"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('token')
    return None

def check_keywords(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/keywords?page=1&size=5", headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

token = login_get_token()
if token:
    check_keywords(token)