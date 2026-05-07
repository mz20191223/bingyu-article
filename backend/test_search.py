import requests

BASE_URL = 'http://localhost:5000/api'

def login():
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'username': 'admin',
        'password': '123456'
    })
    if response.status_code == 200:
        return response.json().get('data', {}).get('token')
    return None

def test_search(token, name):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/prompt-templates?name={name}', headers=headers)
    print(f"搜索 '{name}':")
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回数据: {result}")
    print()

token = login()
if token:
    print(f"Token获取成功: {token[:20]}...")
    print()
    test_search(token, '不存在的模板')
    test_search(token, '')
else:
    print("登录失败")
