import sys
sys.path.insert(0, 'backend')

from app import create_app

app = create_app()

print("已注册的蓝图:")
for name, bp in app.blueprints.items():
    print(f"  {name}: {bp.url_prefix}")

print("\n已注册的所有路由:")
for rule in app.url_map.iter_rules():
    if 'draft' in str(rule):
        print(f"  {rule.endpoint}: {rule}")