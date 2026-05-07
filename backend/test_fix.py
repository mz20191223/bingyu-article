import os
from app.services.image_composite_service import image_composite_service

# 测试JPEG图片合成
test_image_path = r'D:\python project\auto_publish.py\new article\img\微信图片_20260506162206_1364_191.jpg'
if not os.path.exists(test_image_path):
    print(f"测试图片不存在: {test_image_path}")
    exit(1)

text_config = {
    'text': '测试文字',
    'fontSize': 'medium',
    'color': 'white',
    'bgStyle': 'none',
    'positionX': 50,
    'positionY': 50,
    'bold': False
}

try:
    output_path = image_composite_service.composite_text_on_image(test_image_path, text_config)
    print(f"合成成功！输出路径: {output_path}")
except Exception as e:
    print(f"合成失败: {e}")
    import traceback
    traceback.print_exc()
