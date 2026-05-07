import requests
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
        
        # 用户图片路径
        user_image_path = '../img/微信图片_20260506162206_1364_191.jpg'
        
        if not os.path.exists(user_image_path):
            print(f"用户图片不存在: {user_image_path}")
            exit(1)
        
        print(f"\n上传用户图片: {user_image_path}")
        print(f"文件大小: {os.path.getsize(user_image_path)} bytes")
        
        # 上传图片
        with open(user_image_path, 'rb') as f:
            files = {'file': ('test_direct.jpg', f, 'image/jpeg')}
            upload_response = requests.post(
                f'{base_url}/api/images/upload',
                files=files,
                headers={'Authorization': f'Bearer {token}'}
            )
        
        print(f"上传状态码: {upload_response.status_code}")
        print(f"上传响应: {upload_response.text}")
        
        # 检查上传目录
        upload_dir = './static/uploads'
        print(f"\n检查上传目录: {os.path.abspath(upload_dir)}")
        print(f"目录是否存在: {os.path.exists(upload_dir)}")
        
        if os.path.exists(upload_dir):
            files = os.listdir(upload_dir)
            print(f"目录中的文件: {files}")
            
            # 查找最新上传的文件
            latest_file = None
            latest_time = 0
            for f in files:
                if 'test_direct' in f:
                    file_path = os.path.join(upload_dir, f)
                    mtime = os.path.getmtime(file_path)
                    if mtime > latest_time:
                        latest_time = mtime
                        latest_file = f
            
            if latest_file:
                print(f"找到上传的文件: {latest_file}")
                file_path = os.path.join(upload_dir, latest_file)
                print(f"文件路径: {os.path.abspath(file_path)}")
                print(f"文件大小: {os.path.getsize(file_path)} bytes")
            else:
                print("没有找到上传的文件")
    else:
        print(f"登录失败: {login_response.text}")
        
except Exception as e:
    import traceback
    print(f"测试过程中发生错误: {e}")
    traceback.print_exc()
