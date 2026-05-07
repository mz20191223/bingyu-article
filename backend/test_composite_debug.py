import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFont
from app.services.image_composite_service import image_composite_service

# 测试图片路径
test_image_path = r'D:\python project\auto_publish.py\new article\img\微信图片_20260506162206_1364_191.jpg'

if not os.path.exists(test_image_path):
    print(f"测试图片不存在: {test_image_path}")
    exit(1)

# 测试配置
text_config = {
    'text': '088886',
    'fontSize': 'large',
    'color': 'red',
    'bgStyle': 'none',
    'positionX': 45.19,
    'positionY': 28.67,
    'bold': True
}

print(f"=== 测试配置 ===")
print(f"文字内容: {text_config['text']}")
print(f"字体大小: {text_config['fontSize']}")
print(f"颜色: {text_config['color']}")
print(f"位置: ({text_config['positionX']}%, {text_config['positionY']}%)")
print(f"粗体: {text_config['bold']}")

# 打开图片
img = Image.open(test_image_path)
width, height = img.size
print(f"\n=== 图片信息 ===")
print(f"图片尺寸: {width} x {height}")
print(f"图片格式: {img.format}")
print(f"图片模式: {img.mode}")

# 解析配置
text = text_config.get('text', '')
font_size = text_config.get('fontSize', 'medium')
color = text_config.get('color', 'white')
bg_style = text_config.get('bgStyle', 'none')
position_x = text_config.get('positionX', 50)
position_y = text_config.get('positionY', 90)
bold = text_config.get('bold', False)

# 字体大小映射（与前端保持一致）
font_size_map = {
    'small': 16,
    'medium': 24,
    'large': 36
}
font_size_px = font_size_map.get(font_size, 24)

# 颜色映射
color_map = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255)
}
text_color = color_map.get(color, (255, 255, 255))

# 测试不同字体文件
font_path = 'C:/Windows/Fonts/msyh.ttc'
bold_font_path = 'C:/Windows/Fonts/msyhbd.ttc'
print(f"\n=== 字体测试 ===")

# 测试普通字体
try:
    font = ImageFont.truetype(font_path, font_size_px)
    try:
        bbox = font.getbbox(text)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        tw, th = font.getsize(text)
    print(f"普通字体 (msyh.ttc): 文字尺寸 {tw}x{th}")
except Exception as e:
    print(f"普通字体加载失败 - {e}")

# 测试粗体字体
try:
    font_bold = ImageFont.truetype(bold_font_path, font_size_px)
    try:
        bbox = font_bold.getbbox(text)
        tw_bold, th_bold = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except:
        tw_bold, th_bold = font_bold.getsize(text)
    print(f"粗体字体 (msyhbd.ttc): 文字尺寸 {tw_bold}x{th_bold}")
except Exception as e:
    print(f"粗体字体加载失败 - {e}")

# 使用合成服务测试
print(f"\n=== 执行合成 ===")
try:
    output_path = image_composite_service.composite_text_on_image(test_image_path, text_config)
    print(f"合成成功！输出路径: {output_path}")
    print(f"输出文件存在: {os.path.exists(output_path)}")
    
    # 检查输出文件大小
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"输出文件大小: {file_size} bytes")
except Exception as e:
    print(f"合成失败: {e}")
    import traceback
    traceback.print_exc()
