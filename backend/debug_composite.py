import os
from PIL import Image, ImageDraw, ImageFont
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
    'color': 'black',
    'bgStyle': 'none',
    'positionX': 45.45,
    'positionY': 28.67,
    'bold': True
}

# 打开图片查看尺寸
img = Image.open(test_image_path)
print(f"原图尺寸: {img.size}")
width, height = img.size

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
    'small': 14,
    'medium': 20,
    'large': 32
}
font_size_px = font_size_map.get(font_size, 20)

# 设置字体（支持粗体）
font_path = 'C:/Windows/Fonts/msyh.ttc'
try:
    if bold and 'msyh' in font_path.lower():
        font = ImageFont.truetype(font_path, font_size_px, index=1)
        print(f"粗体字体加载成功: {font_path} (index=1)")
    else:
        font = ImageFont.truetype(font_path, font_size_px)
        print(f"字体加载成功: {font_path}")
except Exception as e:
    font = ImageFont.load_default()
    print(f"使用默认字体: {e}")

# 获取文字尺寸
draw = ImageDraw.Draw(img)
try:
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
except AttributeError:
    text_width, text_height = draw.textsize(text, font=font)

print(f"文字尺寸: {text_width} x {text_height}")
print(f"位置百分比: X={position_x}%, Y={position_y}%")

# 计算位置
x = int(width * position_x / 100)
y = int(height * position_y / 100)
print(f"原始位置(未居中): ({x}, {y})")

# 居中调整
x = x - text_width // 2
y = y - text_height // 2
print(f"居中后位置: ({x}, {y})")

# 执行合成
try:
    output_path = image_composite_service.composite_text_on_image(test_image_path, text_config)
    print(f"合成成功！输出路径: {output_path}")
except Exception as e:
    print(f"合成失败: {e}")
    import traceback
    traceback.print_exc()
