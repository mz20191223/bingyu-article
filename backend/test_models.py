import requests

BASE_URL = 'http://localhost:5000/api'

# 登录
login_response = requests.post(f'{BASE_URL}/auth/login', json={
    'username': 'admin',
    'password': '123456'
})
token = login_response.json().get('data', {}).get('token')
headers = {'Authorization': f'Bearer {token}'}

# 检查 AI 模型
print("=== AI 模型列表 ===")
response = requests.get(f'{BASE_URL}/models', headers=headers)
print(f"状态码: {response.status_code}")
result = response.json()
print(f"响应: {result}")
