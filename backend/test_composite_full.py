import os
import json
from PIL import Image, ImageDraw, ImageFont

# 模拟用户配置
overlay_config = {
    'text': '088886',
    'fontSize': 'large',
    'color': 'black',
    'bgStyle': 'none',
    'positionX': 46.46874836206449,
    'positionY': 29.146993667485116,
    'bold': True
}

# 字体大小映射
font_size_map = {
    'small': 16,
    'medium': 24,
    'large': 36
}

# 颜色映射
color_map = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'blue': (0, 0, 255)
}

# 解析配置
text = overlay_config.get('text', '')
font_size = overlay_config.get('fontSize', 'medium')
color = overlay_config.get('color', 'white')
bg_style = overlay_config.get('bgStyle', 'none')
position_x = overlay_config.get('positionX', 50)
position_y = overlay_config.get('positionY', 90)
bold = overlay_config.get('bold', False)

font_size_px = font_size_map.get(font_size, 24)
text_color = color_map.get(color, (255, 255, 255))

print(f"解析后的配置:")
print(f"  text: {text}")
print(f"  fontSize: {font_size} -> {font_size_px}px")
print(f"  color: {color} -> {text_color}")
print(f"  bold: {bold}")
print(f"  position: ({position_x}%, {position_y}%)")

# 字体路径
font_path = 'C:/Windows/Fonts/msyh.ttc'
bold_font_path = 'C:/Windows/Fonts/msyhbd.ttc'

# 打开测试图片（使用用户的图片）
image_path = '../img/微信图片_20260506162206_1364_191.jpg'
if not os.path.exists(image_path):
    print(f"图片不存在: {image_path}")
    exit(1)

img = Image.open(image_path)
width, height = img.size
print(f"\n图片尺寸: {width}x{height}")

# 创建绘制对象
draw = ImageDraw.Draw(img)

# 设置字体
try:
    if bold:
        font = ImageFont.truetype(bold_font_path, font_size_px)
        print(f"使用粗体字体: {bold_font_path}")
    else:
        font = ImageFont.truetype(font_path, font_size_px)
        print(f"使用普通字体: {font_path}")
except Exception as e:
    font = ImageFont.load_default()
    print(f"字体加载失败，使用默认字体: {e}")

# 获取文字尺寸
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
print(f"文字尺寸: {text_width}x{text_height}")

# 计算位置
x = int(width * position_x / 100)
y = int(height * position_y / 100)
x = x - text_width // 2
y = y - text_height // 2
print(f"文字位置: ({x}, {y})")

# 绘制文字
draw.text((x, y), text, font=font, fill=text_color)

# 保存结果
output_path = 'test_composite_result.jpg'
img.convert('RGB').save(output_path)
print(f"\n合成图片已保存到: {output_path}")
