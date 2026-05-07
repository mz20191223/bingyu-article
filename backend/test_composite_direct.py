import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.image_composite_service import image_composite_service

# 测试图片路径
test_image_path = r'D:\python project\auto_publish.py\new article\img\微信图片_20260506162206_1364_191.jpg'

if not os.path.exists(test_image_path):
    print(f"测试图片不存在: {test_image_path}")
    exit(1)

# 测试配置（模拟前端传递的数据）
text_config = {
    'text': '088886',
    'fontSize': 'large',
    'color': 'red',
    'bgStyle': 'none',
    'positionX': 45.19,
    'positionY': 28.67,
    'bold': True
}

print(f"测试配置: {text_config}")
print(f"测试图片: {test_image_path}")

# 执行合成
try:
    output_path = image_composite_service.composite_text_on_image(test_image_path, text_config)
    print(f"合成成功！输出路径: {output_path}")
    print(f"输出文件存在: {os.path.exists(output_path)}")
except Exception as e:
    print(f"合成失败: {e}")
    import traceback
    traceback.print_exc()
