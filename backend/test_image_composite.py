import sys
sys.path.insert(0, '.')

from app import create_app
from app.services.image_composite_service import image_composite_service
import os

app = create_app()

# 测试图片合成服务
test_image_path = '../img/微信图片_20260506162203_1361_191.png'  # 测试图片路径

if os.path.exists(test_image_path):
    print(f"测试图片存在: {test_image_path}")
    
    # 测试文字配置
    text_config = {
        'text': '邀请码：088886',
        'fontSize': 'large',
        'color': 'white',
        'bgStyle': 'transparent',
        'positionX': 50,
        'positionY': 90,
        'bold': True
    }
    
    try:
        output_path = image_composite_service.composite_text_on_image(test_image_path, text_config)
        print(f"合成成功! 输出路径: {output_path}")
        
        if os.path.exists(output_path):
            print("合成图片已保存")
        else:
            print("合成图片保存失败")
            
    except Exception as e:
        print(f"合成失败: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"测试图片不存在: {test_image_path}")
    print("请确认测试图片路径是否正确")