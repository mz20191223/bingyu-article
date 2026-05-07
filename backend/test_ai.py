import requests

BASE_URL = 'http://localhost:5000/api'

def test_ai_generate():
    print("=== 测试 AI 生成接口 ===")

    # 测试没有 token 的情况
    print("\n1. 不带 token 测试:")
    try:
        response = requests.post(f'{BASE_URL}/ai/generate', json={
            'productId': 1,
            'keywords': '省钱,返利,优惠',
            'websiteIds': []
        })
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
    except Exception as e:
        print(f"错误: {e}")

    # 先登录获取 token
    print("\n2. 登录获取 token:")
    login_response = requests.post(f'{BASE_URL}/auth/login', json={
        'username': 'admin',
        'password': '123456'
    })
    if login_response.status_code == 200:
        result = login_response.json()
        token = result.get('data', {}).get('token')
        print(f"Token: {token[:20]}..." if token else "无 token")

        # 用 token 测试
        print("\n3. 带 token 测试:")
        headers = {'Authorization': f'Bearer {token}'}
        try:
            response = requests.post(f'{BASE_URL}/ai/generate', json={
                'productId': 1,
                'keywords': '省钱,返利',
                'websiteIds': []
            }, headers=headers)
            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应 code: {result.get('code')}")
            print(f"响应 msg: {result.get('msg')}")
            if result.get('data'):
                print(f"标题: {result['data'].get('title', '')[:50]}...")
        except Exception as e:
            print(f"错误: {e}")
    else:
        print(f"登录失败: {login_response.status_code}")

if __name__ == '__main__':
    test_ai_generate()
