from app import create_app
from app.models import db, SysMenu

app = create_app()

with app.app_context():
    # 删除旧的内容模板和标题模板菜单
    content_template_menu = SysMenu.query.filter_by(menu_name='内容模板').first()
    title_template_menu = SysMenu.query.filter_by(menu_name='标题模板').first()
    
    if content_template_menu:
        # 删除子菜单（按钮权限）
        SysMenu.query.filter_by(parent_id=content_template_menu.menu_id).delete()
        db.session.delete(content_template_menu)
        print("已删除内容模板菜单")
    
    if title_template_menu:
        # 删除子菜单（按钮权限）
        SysMenu.query.filter_by(parent_id=title_template_menu.menu_id).delete()
        db.session.delete(title_template_menu)
        print("已删除标题模板菜单")
    
    # 检查是否已存在提示词模板菜单
    prompt_template_menu = SysMenu.query.filter_by(menu_name='提示词模板').first()
    
    if not prompt_template_menu:
        # 获取AI配置父菜单ID
        ai_config_menu = SysMenu.query.filter_by(menu_name='AI配置').first()
        
        if ai_config_menu:
            # 创建提示词模板菜单
            prompt_template = SysMenu(
                menu_name='提示词模板',
                menu_type='C',
                path='/ai-config/prompt-template',
                component='ai-config/prompt-template/index',
                parent_id=ai_config_menu.menu_id,
                menu_sort=3,
                status=0
            )
            db.session.add(prompt_template)
            db.session.flush()
            
            # 创建按钮权限
            buttons = [
                {'menu_name': '模板新增', 'menu_type': 'F', 'perms': 'ai:prompt:add', 'menu_sort': 1},
                {'menu_name': '模板编辑', 'menu_type': 'F', 'perms': 'ai:prompt:edit', 'menu_sort': 2},
                {'menu_name': '模板删除', 'menu_type': 'F', 'perms': 'ai:prompt:delete', 'menu_sort': 3},
                {'menu_name': '模板查询', 'menu_type': 'F', 'perms': 'ai:prompt:query', 'menu_sort': 4},
            ]
            
            for btn in buttons:
                button_menu = SysMenu(
                    menu_name=btn['menu_name'],
                    menu_type=btn['menu_type'],
                    perms=btn['perms'],
                    parent_id=prompt_template.menu_id,
                    menu_sort=btn['menu_sort'],
                    status=0
                )
                db.session.add(button_menu)
            
            print("已创建提示词模板菜单及按钮权限")
    
    db.session.commit()
    print("菜单更新完成！")