import os
import sys
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.image_composite_service import image_composite_service

# 测试配置
overlay_config = {
    'text': 'TEST088886',
    'fontSize': 'large',
    'color': 'red',
    'bgStyle': 'none',
    'positionX': 50,
    'positionY': 50,
    'bold': True
}

# 测试图片路径
test_image_path = '../img/微信图片_20260506162206_1364_191.jpg'

print(f"测试图片路径: {test_image_path}")
print(f"图片是否存在: {os.path.exists(test_image_path)}")
print(f"配置: {json.dumps(overlay_config, indent=2)}")

if not os.path.exists(test_image_path):
    print("测试图片不存在！")
    exit(1)

# 创建输出目录
output_dir = 'test_output'
os.makedirs(output_dir, exist_ok=True)

# 生成输出路径
base_name = os.path.basename(test_image_path)
name, ext = os.path.splitext(base_name)
output_path = os.path.join(output_dir, f"{name}_with_text{ext}")

print(f"\n输出路径: {output_path}")

try:
    # 直接调用合成服务
    result = image_composite_service.composite_text_on_image(test_image_path, overlay_config, output_path)
    print(f"合成成功！结果路径: {result}")
    print(f"生成的文件是否存在: {os.path.exists(result)}")
    
    if os.path.exists(result):
        file_size = os.path.getsize(result)
        print(f"文件大小: {file_size} bytes")
except Exception as e:
    import traceback
    print(f"合成失败: {e}")
    traceback.print_exc()
