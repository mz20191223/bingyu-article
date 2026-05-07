import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_login():
    """登录获取token"""
    login_data = {"username": "admin", "password": "123456"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('token')
    return None

def generate_content(token, product_id, keywords):
    """调用AI生成标题和内容"""
    headers = {"Authorization": f"Bearer {token}"}
    
    generate_data = {
        "productId": product_id,
        "keywordIds": [],
        "keywords": keywords,
        "modelId": None
    }
    
    print(f"正在调用AI生成内容，关键词: {keywords}")
    response = requests.post(f"{BASE_URL}/ai/generate", json=generate_data, headers=headers)
    print(f"AI生成响应状态: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 200:
            data = result.get('data', {})
            title = data.get('title', '')
            content = data.get('content', '')
            print(f"AI生成成功！")
            print(f"标题: {title}")
            print(f"内容长度: {len(content)}")
            return title, content
    
    print(f"AI生成失败: {response.text}")
    return None, None

def publish_article(token, product_id, website_id, title, content):
    """发布文章"""
    headers = {"Authorization": f"Bearer {token}"}
    
    publish_data = {
        "title": title,
        "content": content,
        "productId": product_id,
        "websiteIds": [website_id]
    }
    
    print(f"\n正在发布文章...")
    response = requests.post(f"{BASE_URL}/publish/submit", json=publish_data, headers=headers)
    print(f"发布响应状态: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 200:
            print(f"发布成功!")
            return result.get('data')
    
    print(f"发布失败: {response.text}")
    return None

def get_publish_records(token, limit=5):
    """获取发布记录"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/records?page=1&size={limit}", headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('list', [])
    return []

def main():
    print("=" * 50)
    print("开始测试文章发布流程")
    print("=" * 50)
    
    # 1. 登录
    token = test_login()
    if not token:
        print("登录失败!")
        return
    
    print(f"登录成功!\n")
    
    # 2. 获取产品和网站信息
    headers = {"Authorization": f"Bearer {token}"}
    
    # 获取网站
    response = requests.get(f"{BASE_URL}/websites", headers=headers)
    websites = response.json().get('data', {}).get('list', [])
    if not websites:
        print("没有找到网站")
        return
    website = websites[0]  # 使用第一个网站 (有目网)
    print(f"使用网站: {website.get('name')} (ID: {website.get('id')})")
    
    # 获取产品
    response = requests.get(f"{BASE_URL}/products", headers=headers)
    products = response.json().get('data', {}).get('list', [])
    if not products:
        print("没有找到产品")
        return
    product = products[0]  # 使用第一个产品 (高省)
    print(f"使用产品: {product.get('name')} (ID: {product.get('id')})\n")
    
    # 3. 调用AI生成标题和内容
    title, content = generate_content(token, product.get('id'), "高省返利APP")
    if not title or not content:
        print("AI生成失败，测试终止")
        return
    
    # 4. 发布文章
    publish_result = publish_article(token, product.get('id'), website.get('id'), title, content)
    if not publish_result:
        print("发布失败，测试终止")
        return
    
    # 5. 获取发布记录，查看返回的文章链接
    print("\n获取发布记录...")
    time.sleep(2)  # 等待一下让后端处理完成
    
    records = get_publish_records(token, limit=3)
    if records:
        print("\n最新发布记录:")
        for i, record in enumerate(records[:3]):
            print(f"\n记录 {i+1}:")
            print(f"  标题: {record.get('title')}")
            print(f"  状态: {record.get('status')}")
            print(f"  文章链接: {record.get('result_url')}")
            print(f"  发布时间: {record.get('publish_time')}")
    else:
        print("没有找到发布记录")
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    main()