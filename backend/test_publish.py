"""
测试文章发布功能 - 手动发布模式
"""
import requests

base_url = 'http://127.0.0.1:5000'

test_title = "高省APP：开启你的省钱之旅"
test_content = """<p>高省APP是一款全新的优惠券领取平台，让您的每一次购物都能省钱！</p>

<p>【产品特色】</p>
<p>✅ 海量优惠券实时更新</p>
<p>✅ 一键领取，自动抵扣</p>
<p>✅ 邀请好友还能赚佣金</p>

<p>【使用方法】</p>
<p>1. 下载并安装高省APP</p>
<p>2. 注册成为会员</p>
<p>3. 搜索心仪商品</p>
<p>4. 领取优惠券下单</p>

<p>立即下载高省APP，开启您的省钱之旅吧！</p>"""

login_data = {
    'username': 'admin',
    'password': '123456'
}

try:
    print("=== 登录 ===")
    login_response = requests.post(f'{base_url}/api/auth/login', json=login_data)
    print(f"登录状态码: {login_response.status_code}")

    if login_response.status_code == 200:
        token = login_response.json().get('data', {}).get('token')
        print(f"获取到token: {token[:20]}...")

        headers = {'Authorization': f'Bearer {token}'}

        print("\n=== 获取产品列表 ===")
        products_response = requests.get(f'{base_url}/api/products', headers=headers, params={'pageSize': 100})
        products = products_response.json().get('data', {}).get('list', [])
        print(f"产品数量: {len(products)}")
        if products:
            product = products[0]
            print(f"选择产品: ID={product['id']}, 名称={product['name']}")

        print("\n=== 发布文章到有目网 ===")
        print(f"标题: {test_title}")
        print(f"内容长度: {len(test_content)} 字符")

        publish_response = requests.post(
            f'{base_url}/api/publish/submit',
            headers=headers,
            json={
                'productId': product['id'],
                'websiteIds': [6],
                'title': test_title,
                'content': test_content
            }
        )
        print(f"发布状态码: {publish_response.status_code}")
        publish_result = publish_response.json()
        print(f"发布响应: {publish_result}")

        if publish_result.get('code') == 200:
            print("\n✅ 文章发布成功！")
        else:
            print(f"\n❌ 发布失败: {publish_result.get('msg', '未知错误')}")

    else:
        print(f"登录失败: {login_response.text}")

except Exception as e:
    import traceback
    print(f"测试过程中发生错误: {e}")
    traceback.print_exc()