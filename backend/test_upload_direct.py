import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
import json

app = create_app()

# 使用测试客户端
client = app.test_client()

# 先登录
login_data = {
    'username': 'admin',
    'password': '123456'
}

login_response = client.post('/api/auth/login', json=login_data)
print(f"登录状态码: {login_response.status_code}")
login_result = login_response.get_json()
token = login_result.get('data', {}).get('token')
print(f"获取到token: {token[:20]}...")

# 准备测试图片
test_image_path = '../img/微信图片_20260506162206_1364_191.jpg'
if not os.path.exists(test_image_path):
    print(f"测试图片不存在: {test_image_path}")
    exit(1)

print(f"\n测试图片路径: {test_image_path}")
print(f"文件大小: {os.path.getsize(test_image_path)} bytes")

# 读取图片内容
with open(test_image_path, 'rb') as f:
    image_data = f.read()

# 上传图片
headers = {'Authorization': f'Bearer {token}'}
data = {
    'file': (os.path.basename(test_image_path), image_data, 'image/jpeg')
}

upload_response = client.post('/api/images/upload', data=data, headers=headers, content_type='multipart/form-data')
print(f"\n上传状态码: {upload_response.status_code}")
print(f"上传响应: {upload_response.data.decode('utf-8')}")

# 检查上传目录
upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
print(f"\n上传目录: {upload_dir}")
print(f"目录是否存在: {os.path.exists(upload_dir)}")

if os.path.exists(upload_dir):
    files = os.listdir(upload_dir)
    print(f"目录中的文件: {files}")
