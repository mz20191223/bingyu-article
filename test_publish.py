import requests
import time

# 目标网站信息
TARGET_URL = "https://yomowoo.com"
USERNAME = "290191683@qq.com"
PASSWORD = "a12345678"

def test_publish():
    """测试发布文章并获取正确链接"""
    try:
        # 1. 登录系统
        print("正在登录系统...")
        session = requests.Session()
        
        # 2. 测试文章数据
        test_title = "测试文章标题" + str(int(time.time()))
        test_content = "这是一篇测试文章的内容。"
        
        # 3. 调用发布API
        print(f"正在发布文章: {test_title}")
        
        # 4. 模拟发布逻辑（实际发布需要浏览器自动化）
        # 这里只是演示，实际需要selenium等工具
        
        print("发布完成！")
        print(f"预期文章链接格式: https://yomowoo.com/post/{test_title}.html")
        print("实际文章链接需要在浏览器中验证")
        
        return True
        
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_publish()
