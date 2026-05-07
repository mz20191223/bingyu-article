import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import SysMenu

app = create_app()
with app.app_context():
    parent = SysMenu.query.filter_by(menu_name='文章管理').first()
    if not parent:
        print("文章管理菜单不存在")
    else:
        existing = SysMenu.query.filter_by(menu_name='草稿管理').first()
        if existing:
            print(f"草稿管理已存在: ID {existing.menu_id}")
        else:
            menu = SysMenu(
                menu_name='草稿管理',
                menu_type='C',
                path='/article/draft',
                component='article/draft/index',
                parent_id=parent.menu_id,
                menu_sort=3
            )
            db.session.add(menu)
            db.session.commit()
            print(f"已创建草稿管理菜单: ID {menu.menu_id}, parent_id: {parent.menu_id}")

        children = SysMenu.query.filter_by(parent_id=parent.menu_id).all()
        print(f"\n文章管理的子菜单 ({len(children)}):")
        for c in children:
            print(f"  - {c.menu_name} (ID: {c.menu_id}, path: {c.path})")