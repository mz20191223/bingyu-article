import requests

BASE_URL = "http://127.0.0.1:5000"

def login():
    login_data = {
        "username": "admin",
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print(f"登录状态码: {response.status_code}")
    print(f"登录结果: {response.text}")
    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('token')
    return None

def test_create_model(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    model_data = {
        "name": "智谱",
        "provider": "zhipuai",
        "apiKey": "06dc22a38ba04b19bb0c381bab2e73a2.xo3BOb0khrMfCsrq",
        "apiUrl": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "modelName": "GLM-4.5-Air",
        "status": 0
    }
    
    response = requests.post(f"{BASE_URL}/api/models", json=model_data, headers=headers)
    print(f"创建模型状态码: {response.status_code}")
    print(f"创建模型结果: {response.text}")
    return response

if __name__ == "__main__":
    print("=== 测试 AI 模型 API ===")
    
    token = login()
    if token:
        print("登录成功")
        test_create_model(token)
    else:
        print("登录失败")