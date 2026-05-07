import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from app.services.image_composite_service import image_composite_service

# 测试图片路径
test_image_path = r'D:\python project\auto_publish.py\new article\img\微信图片_20260506162206_1364_191.jpg'

if not os.path.exists(test_image_path):
    print(f"测试图片不存在: {test_image_path}")
    exit(1)

# 测试不同字体大小
font_sizes = ['small', 'medium', 'large']

for size in font_sizes:
    print(f"\n=== 测试字体大小: {size} ===")
    
    # 模拟前端发送的数据格式
    text_overlay = json.dumps({
        'text': '088886',
        'fontSize': size,
        'color': 'red',
        'bgStyle': 'none',
        'positionX': 50,
        'positionY': 50,
        'bold': False
    })
    
    # 解析配置（模拟后端解析）
    overlay_config = json.loads(text_overlay)
    print(f"解析后的配置: {overlay_config}")
    
    # 执行合成
    try:
        output_path = image_composite_service.composite_text_on_image(test_image_path, overlay_config)
        print(f"合成成功！输出路径: {output_path}")
        
        # 检查文件大小（可以反映字体大小）
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"输出文件大小: {file_size} bytes")
    except Exception as e:
        print(f"合成失败: {e}")
