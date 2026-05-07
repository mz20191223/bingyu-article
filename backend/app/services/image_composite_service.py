import os
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap

class ImageCompositeService:
    """图片合成服务 - 在图片上叠加文字"""
    
    def __init__(self):
        # 默认字体路径（使用系统字体）
        self.font_path = self._get_default_font()
        
    def _get_default_font(self):
        """获取默认字体路径"""
        # Windows系统字体路径
        font_paths = [
            'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
            'C:/Windows/Fonts/simsun.ttc',  # 宋体
            'C:/Windows/Fonts/arial.ttf',   # Arial
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
        return None
    
    def composite_text_on_image(self, image_path, text_config, output_path=None):
        """
        在图片上合成文字
        
        Args:
            image_path: 原图路径
            text_config: 文字配置字典
            output_path: 输出路径，不指定则自动生成
        
        Returns:
            合成后图片的路径
        """
        if not os.path.exists(image_path):
            raise ValueError(f"图片不存在: {image_path}")
        
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
        
        # 背景样式映射
        bg_opacity_map = {
            'none': 0,
            'transparent': 128,  # 半透明
            'solid': 200  # 全透明
        }
        bg_opacity = bg_opacity_map.get(bg_style, 0)
        
        # 打开图片（先保持原始格式，避免不必要的转换）
        img = Image.open(image_path)
        width, height = img.size
        
        # 如果图片不是RGBA模式且需要透明度效果，才转换
        needs_alpha = bg_opacity > 0
        if needs_alpha and img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 创建绘制对象
        draw = ImageDraw.Draw(img)
        
        # 设置字体（支持粗体）
        try:
            if bold:
                # 尝试加载粗体字体
                if self.font_path and 'msyh' in self.font_path.lower():
                    # 微软雅黑粗体使用专门的粗体文件 msyhbd.ttc
                    bold_font_path = self.font_path.replace('msyh.ttc', 'msyhbd.ttc')
                    font = ImageFont.truetype(bold_font_path, font_size_px)
                elif self.font_path and 'simsun' in self.font_path.lower():
                    # 宋体粗体在 index=1
                    font = ImageFont.truetype(self.font_path, font_size_px, index=1)
                else:
                    # 其他字体尝试使用默认粗体
                    font = ImageFont.truetype(self.font_path, font_size_px)
            else:
                font = ImageFont.truetype(self.font_path, font_size_px)
        except Exception as e:
            # 如果粗体加载失败，回退到普通字体
            try:
                font = ImageFont.truetype(self.font_path, font_size_px)
            except:
                font = ImageFont.load_default()
        
        # 获取文字尺寸（兼容新旧版本Pillow）
        try:
            # 新版本 Pillow 使用 textbbox
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # 旧版本 Pillow 使用 textsize
            text_width, text_height = draw.textsize(text, font=font)
        
        # 计算文字位置（百分比转像素，考虑居中）
        # 使用 transform: translate(-50%, -50%) 的效果
        x = int(width * position_x / 100)
        y = int(height * position_y / 100)
        
        # 减去文字宽高的一半，实现居中效果
        x = x - text_width // 2
        y = y - text_height // 2
        
        # 如果有背景，先绘制背景
        if bg_opacity > 0:
            bg_padding = 10
            bg_width = text_width + bg_padding * 2
            bg_height = text_height + bg_padding * 2
            bg_x = x - bg_padding
            bg_y = y - bg_padding
            
            # 创建背景层
            bg_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            bg_draw = ImageDraw.Draw(bg_layer)
            bg_draw.rectangle(
                [bg_x, bg_y, bg_x + bg_width, bg_y + bg_height],
                fill=(0, 0, 0, bg_opacity)
            )
            img = Image.alpha_composite(img, bg_layer)
            draw = ImageDraw.Draw(img)
        
        # 绘制文字
        draw.text((x, y), text, font=font, fill=text_color)
        
        # 生成输出路径
        if output_path is None:
            dir_name = os.path.dirname(image_path)
            base_name = os.path.basename(image_path)
            name, ext = os.path.splitext(base_name)
            output_path = os.path.join(dir_name, f"{name}_with_text{ext}")
        
        # 保存图片（处理JPEG不支持RGBA的问题）
        _, ext = os.path.splitext(output_path)
        if ext.lower() in ['.jpg', '.jpeg']:
            # JPEG不支持透明度，转换为RGB模式
            img = img.convert('RGB')
        
        img.save(output_path)
        
        return output_path
    
    def generate_composite(self, image_url, text_config):
        """
        生成合成图片
        
        Args:
            image_url: 图片URL或本地路径
            text_config: 文字配置JSON字符串或字典
        
        Returns:
            合成后图片的URL
        """
        # 如果是JSON字符串，解析为字典
        if isinstance(text_config, str):
            try:
                text_config = json.loads(text_config)
            except json.JSONDecodeError:
                raise ValueError("text_config不是有效的JSON")
        
        # 如果是URL，先下载到本地
        if image_url.startswith('http://') or image_url.startswith('https://'):
            # 从URL提取文件名
            import urllib.parse
            parsed = urllib.parse.urlparse(image_url)
            local_path = os.path.join('static/images', os.path.basename(parsed.path))
            
            # 下载图片
            import urllib.request
            os.makedirs('static/images', exist_ok=True)
            urllib.request.urlretrieve(image_url, local_path)
            image_path = local_path
        else:
            image_path = image_url
        
        # 生成合成图片
        output_path = self.composite_text_on_image(image_path, text_config)
        
        # 返回合成后的路径
        return output_path

# 单例
image_composite_service = ImageCompositeService()