from app import create_app
from flask import Request
import json

app = create_app()

# 模拟用户请求
test_data = {
    'productId': 1,
    'keywords': '京东返利app叫什么',
    'websiteIds': [6]
}

with app.app_context():
    # 模拟请求对象
    class MockRequest:
        def get_json(self):
            return test_data
    
    # 导入路由函数
    from app.routes.ai import generate_content
    
    # 设置模拟请求
    import flask
    flask.request = MockRequest()
    
    # 调用路由函数
    print('=== 模拟用户请求 ===')
    print(f'请求数据: {test_data}')
    print()
    
    try:
        response = generate_content()
        print(f'响应: {response.data.decode("utf-8")}')
    except Exception as e:
        print(f'错误: {e}')
        import traceback
        traceback.print_exc()
