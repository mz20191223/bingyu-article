import os
import sys

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入模块来检查 UPLOAD_FOLDER 的实际值
from app.routes.images import UPLOAD_FOLDER

print(f"UPLOAD_FOLDER 的值: {UPLOAD_FOLDER}")
print(f"UPLOAD_FOLDER 是否存在: {os.path.exists(UPLOAD_FOLDER)}")

# 检查目录中的文件
if os.path.exists(UPLOAD_FOLDER):
    files = os.listdir(UPLOAD_FOLDER)
    print(f"目录中的文件: {files}")

# 测试计算
current_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'routes', 'images.py')
print(f"\nimages.py 的路径: {current_file}")
print(f"dirname x1: {os.path.dirname(current_file)}")  # routes
print(f"dirname x2: {os.path.dirname(os.path.dirname(current_file))}")  # app
print(f"dirname x3: {os.path.dirname(os.path.dirname(os.path.dirname(current_file)))}")  # backend
