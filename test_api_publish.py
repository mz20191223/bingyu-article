import requests
import json
import time

# 系统API地址
BASE_URL = "http://localhost:5000"

def get_token():
    """获取登录token"""
    login_data = {
        "username": "admin",
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('token')
    return None

def test_article_publish():
    """测试文章发布功能"""
    token = get_token()
    if not token:
        print("登录失败")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. 获取网站列表
    print("获取网站列表...")
    response = requests.get(f"{BASE_URL}/websites", headers=headers)
    if response.status_code == 200:
        websites = response.json().get('data', {}).get('list', [])
        if websites:
            website = websites[0]
            print(f"使用网站: {website.get('name')}")
    
    # 2. 获取产品列表
    print("获取产品列表...")
    response = requests.get(f"{BASE_URL}/products", headers=headers)
    if response.status_code == 200:
        products = response.json().get('data', {}).get('list', [])
        if products:
            product = products[0]
            print(f"使用产品: {product.get('name')}")
    
    # 3. 创建测试文章数据
    test_title = "测试文章标题_" + str(int(time.time()))
    test_content = "这是一篇测试文章的内容，用于验证文章链接获取功能。\n\n文章内容第二段落。"
    
    article_data = {
        "title": test_title,
        "content": test_content,
        "product_id": product.get('id'),
        "website_ids": [website.get('id')],
        "keywords": "测试关键词"
    }
    
    print(f"\n准备发布文章: {test_title}")
    print(f"内容长度: {len(test_content)}")
    
    # 4. 调用发布API
    print("正在发布文章...")
    response = requests.post(f"{BASE_URL}/articles/publish", json=article_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n发布结果: {result.get('msg')}")
        
        if result.get('data'):
            article_url = result.get('data').get('article_url')
            print(f"返回的文章链接: {article_url}")
            
            # 验证链接格式
            if article_url and "/post/" in article_url and ".html" in article_url:
                print("✅ 文章链接格式正确！")
            else:
                print("❌ 文章链接格式不正确")
                print(f"期望格式: https://yomowoo.com/post/数字.html")
                print(f"实际格式: {article_url}")
    else:
        print(f"发布失败: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_article_publish()