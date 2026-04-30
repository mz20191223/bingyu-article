from app import create_app, db

app = create_app()
with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    
    table_comments = {
        'sys_user': '系统用户表',
        'sys_role': '角色表',
        'sys_dept': '部门表',
        'sys_post': '岗位表',
        'sys_menu': '菜单表',
        'sys_role_menu': '角色菜单关联表',
        'sys_user_role': '用户角色关联表',
        'sys_login_log': '登录日志表',
        'sys_oper_log': '操作日志表',
        'products': '产品表',
        'websites': '网站配置表',
        'images': '图片管理表',
        'keywords': '关键词表',
        'publish_records': '发布记录表',
        'models': 'AI模型表',
        'content_prompt_templates': '内容模板表',
        'title_prompt_templates': '标题模板表'
    }
    
    for table_name in tables:
        comment = table_comments.get(table_name, '未定义')
        sql = f"ALTER TABLE `{table_name}` COMMENT = '{comment}'"
        try:
            db.engine.execute(sql)
            print(f"✓ {table_name}: {comment}")
        except Exception as e:
            print(f"✗ {table_name}: 添加注释失败 - {str(e)}")

print('\n所有表注释添加完成！')