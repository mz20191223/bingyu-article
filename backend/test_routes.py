import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

# 打印所有注册的路由
print("=== 注册的路由 ===")
for rule in app.url_map.iter_rules():
    print(f"{rule.methods} {rule.rule}")
