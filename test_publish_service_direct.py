import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.services.publish_service import publish_with_playwright

app = create_app()
with app.app_context():
    try:
        print("=" * 50)
        print("直接调用 publish_service 测试")
        print("=" * 50)

        title = "测试直接调用service_" + str(int(__import__('time').time()))
        content = "测试内容"

        result = publish_with_playwright(
            title=title,
            content=content,
            website_id=6,
            user_id=1
        )

        print(f"\n返回结果: {result}")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()