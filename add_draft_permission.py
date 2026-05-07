import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import SysMenu, SysRoleMenu

app = create_app()
with app.app_context():
    menu = SysMenu.query.filter_by(menu_name='草稿管理').first()
    if not menu:
        print("草稿管理菜单不存在")
    else:
        role_menus = SysRoleMenu.query.filter_by(menu_id=menu.menu_id).all()
        print(f"草稿管理菜单 (ID: {menu.menu_id}) 的角色权限数量: {len(role_menus)}")

        if len(role_menus) == 0:
            role_menus_admin = SysRoleMenu.query.filter_by(role_id=1).all()
            print(f"管理员 (role_id=1) 现有菜单权限数量: {len(role_menus_admin)}")

            rm = SysRoleMenu(role_id=1, menu_id=menu.menu_id)
            db.session.add(rm)
            db.session.commit()
            print(f"已给管理员添加草稿管理菜单权限")
        else:
            print("已有角色权限，无需添加")