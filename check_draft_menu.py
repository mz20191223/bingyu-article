import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import SysMenu

app = create_app()
with app.app_context():
    menus = SysMenu.query.filter_by(menu_name='草稿管理').all()
    print(f"找到 {len(menus)} 个草稿管理菜单")
    for m in menus:
        print(f"  ID: {m.menu_id}, 名称: {m.menu_name}, 路径: {m.path}")

    parent = SysMenu.query.filter_by(menu_name='文章管理').first()
    if parent:
        print(f"\n文章管理菜单ID: {parent.menu_id}")
        children = SysMenu.query.filter_by(parent_id=parent.menu_id).all()
        print(f"文章管理的子菜单:")
        for c in children:
            print(f"  - {c.menu_name} (ID: {c.menu_id}, path: {c.path})")