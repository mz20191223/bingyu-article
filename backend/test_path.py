import os

# 测试路径计算
current_file = __file__
print(f"当前文件路径: {current_file}")
print(f"当前文件绝对路径: {os.path.abspath(current_file)}")

# 模拟 images.py 的路径计算
images_py_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'routes', 'images.py')
print(f"\n模拟 images.py 路径: {images_py_path}")

# UPLOAD_FOLDER 的计算
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(images_py_path))), 'static', 'uploads')
print(f"\nUPLOAD_FOLDER: {UPLOAD_FOLDER}")
print(f"UPLOAD_FOLDER 是否存在: {os.path.exists(UPLOAD_FOLDER)}")

# 创建测试文件
test_file_path = os.path.join(UPLOAD_FOLDER, 'test_write.txt')
print(f"\n测试文件路径: {test_file_path}")

try:
    with open(test_file_path, 'w') as f:
        f.write('test content')
    print(f"文件写入成功")
    print(f"文件是否存在: {os.path.exists(test_file_path)}")
    if os.path.exists(test_file_path):
        print(f"文件大小: {os.path.getsize(test_file_path)} bytes")
except Exception as e:
    print(f"文件写入失败: {e}")

# 检查目录中的文件
if os.path.exists(UPLOAD_FOLDER):
    files = os.listdir(UPLOAD_FOLDER)
    print(f"\n目录中的文件: {files}")
