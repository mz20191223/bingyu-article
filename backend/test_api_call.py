import requests
import json

# 后端API地址
base_url = 'http://127.0.0.1:5000'

# 登录获取token
login_data = {
    'username': 'admin',
    'password': '123456'
}

try:
    # 登录
    login_response = requests.post(f'{base_url}/api/auth/login', json=login_data)
    print(f"登录状态码: {login_response.status_code}")
    if login_response.status_code == 200:
        token = login_response.json().get('data', {}).get('token')
        print(f"获取到token: {token[:20]}...")
        
        # 设置请求头
        headers = {'Authorization': f'Bearer {token}'}
        
        # 获取图片列表
        images_response = requests.get(f'{base_url}/api/images', headers=headers)
        print(f"\n获取图片列表状态码: {images_response.status_code}")
        if images_response.status_code == 200:
            images = images_response.json().get('data', {}).get('list', [])
            if images:
                # 使用第一张图片进行测试
                test_image = images[0]
                image_id = test_image['id']
                print(f"测试图片ID: {image_id}")
                print(f"测试图片URL: {test_image['url']}")
                
                # 准备合成参数
                composite_data = {
                    'text_overlay': json.dumps({
                        'text': 'TEST088886',
                        'fontSize': 'large',
                        'color': 'red',
                        'bgStyle': 'none',
                        'positionX': 50,
                        'positionY': 50,
                        'bold': True
                    })
                }
                
                print(f"\n发送合成请求...")
                print(f"合成参数: {composite_data}")
                
                # 调用合成API
                composite_response = requests.put(
                    f'{base_url}/api/images/{image_id}/composite',
                    json=composite_data,
                    headers=headers
                )
                
                print(f"\n合成请求状态码: {composite_response.status_code}")
                print(f"合成响应: {composite_response.text}")
                
                if composite_response.status_code == 200:
                    result = composite_response.json()
                    composite_url = result.get('data', {}).get('compositeUrl')
                    print(f"合成成功！合成图片URL: {composite_url}")
                else:
                    print(f"合成失败: {composite_response.text}")
            else:
                print("没有找到测试图片")
        else:
            print(f"获取图片列表失败: {images_response.text}")
    else:
        print(f"登录失败: {login_response.text}")
        
except Exception as e:
    print(f"测试过程中发生错误: {e}")
