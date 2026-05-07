import requests

BASE_URL = "http://localhost:5000/api"

login_data = {"username": "admin", "password": "123456"}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json().get('data', {}).get('token')
headers = {"Authorization": f"Bearer {token}"}

# 尝试不同的路径
paths = ['/drafts', '/drafts/', '/api/drafts', '/api/drafts/']
for p in paths:
    response = requests.get(f"http://localhost:5000{p}", headers=headers)
    print(f"GET {p}: {response.status_code}")