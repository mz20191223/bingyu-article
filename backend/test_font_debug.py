import os
from PIL import Image, ImageDraw, ImageFont

# 测试字体路径
font_path = 'C:/Windows/Fonts/msyh.ttc'
bold_font_path = 'C:/Windows/Fonts/msyhbd.ttc'

print(f"普通字体路径存在: {os.path.exists(font_path)}")
print(f"粗体字体路径存在: {os.path.exists(bold_font_path)}")

# 创建测试图片
img = Image.new('RGB', (800, 484), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# 测试不同字体大小
test_font_sizes = {'small': 16, 'medium': 24, 'large': 36}

for name, size in test_font_sizes.items():
    # 测试普通字体
    try:
        font = ImageFont.truetype(font_path, size)
        bbox = draw.textbbox((0, 0), '088886', font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        print(f"普通字体 {name}({size}px): 尺寸 {text_width}x{text_height}")
        
        # 绘制测试文字
        draw.text((50, 50 + size * 3), f'普通 {name}: 088886', font=font, fill=(0, 0, 0))
    except Exception as e:
        print(f"普通字体 {name} 加载失败: {e}")
    
    # 测试粗体字体
    try:
        bold_font = ImageFont.truetype(bold_font_path, size)
        bbox = draw.textbbox((0, 0), '088886', font=bold_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        print(f"粗体字体 {name}({size}px): 尺寸 {text_width}x{text_height}")
        
        # 绘制测试文字
        draw.text((400, 50 + size * 3), f'粗体 {name}: 088886', font=bold_font, fill=(255, 0, 0))
    except Exception as e:
        print(f"粗体字体 {name} 加载失败: {e}")

# 保存测试图片
output_path = 'test_font_debug.png'
img.save(output_path)
print(f"\n测试图片已保存到: {output_path}")
