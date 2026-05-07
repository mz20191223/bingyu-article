import requests
import json
import os

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
        
        # 先上传用户的测试图片
        user_image_path = '../img/微信图片_20260506162206_1364_191.jpg'
        
        if not os.path.exists(user_image_path):
            print(f"用户图片不存在: {user_image_path}")
            exit(1)
        
        print(f"\n上传用户图片: {user_image_path}")
        
        with open(user_image_path, 'rb') as f:
            files = {'file': ('test_image.jpg', f, 'image/jpeg')}
            upload_response = requests.post(
                f'{base_url}/api/images/upload',
                files=files,
                headers={'Authorization': f'Bearer {token}'}
            )
        
        print(f"上传状态码: {upload_response.status_code}")
        print(f"上传响应: {upload_response.text}")
        
        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            image_url = upload_result.get('data', {}).get('url')
            print(f"上传成功！图片URL: {image_url}")
            
            # 创建图片记录
            create_data = {
                'url': image_url,
                'positionType': 'auto',
                'status': 0,
                'productIds': []
            }
            
            create_response = requests.post(
                f'{base_url}/api/images',
                json=create_data,
                headers=headers
            )
            
            print(f"\n创建图片记录状态码: {create_response.status_code}")
            print(f"创建响应: {create_response.text}")
            
            if create_response.status_code == 200:
                # 获取图片ID
                images_response = requests.get(f'{base_url}/api/images', headers=headers)
                images = images_response.json().get('data', {}).get('list', [])
                
                if images:
                    # 使用最后上传的图片
                    test_image = images[-1]
                    image_id = test_image['id']
                    print(f"\n测试图片ID: {image_id}")
                    print(f"测试图片URL: {test_image['url']}")
                    
                    # 准备合成参数（模拟用户的实际配置）
                    composite_data = {
                        'text_overlay': json.dumps({
                            'text': '088886',
                            'fontSize': 'large',
                            'color': 'red',
                            'bgStyle': 'none',
                            'positionX': 46.47,
                            'positionY': 29.15,
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
                        
                        # 检查文件是否存在
                        expected_path = f"./static/images/{os.path.basename(composite_url)}"
                        print(f"期望的文件路径: {os.path.abspath(expected_path)}")
                        print(f"文件是否存在: {os.path.exists(expected_path)}")
                    else:
                        print(f"合成失败: {composite_response.text}")
                else:
                    print("没有找到图片列表")
            else:
                print(f"创建图片记录失败: {create_response.text}")
        else:
            print(f"上传图片失败: {upload_response.text}")
    else:
        print(f"登录失败: {login_response.text}")
        
except Exception as e:
    import traceback
    print(f"测试过程中发生错误: {e}")
    traceback.print_exc()
