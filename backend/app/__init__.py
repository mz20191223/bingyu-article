import os
import sys
from flask import Flask
from flask_cors import CORS
from app.config import config
from app.models import db


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)

    with app.app_context():
        db.create_all()
        init_data()

    register_blueprints(app)
    register_handlers(app)

    return app


def register_blueprints(app):
    from app.routes import auth, users, products, images, keywords, templates, models as models_bp, websites, publish, records, logs, roles, dept, menus

    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(users.bp, url_prefix='/api/users')
    app.register_blueprint(products.bp, url_prefix='/api/products')
    app.register_blueprint(images.bp, url_prefix='/api/images')
    app.register_blueprint(keywords.bp, url_prefix='/api/keywords')
    app.register_blueprint(templates.content_bp, url_prefix='/api/content-templates')
    app.register_blueprint(templates.title_bp, url_prefix='/api/title-templates')
    app.register_blueprint(models_bp.bp, url_prefix='/api/models')
    app.register_blueprint(websites.bp, url_prefix='/api/websites')
    app.register_blueprint(publish.bp, url_prefix='/api/publish')
    app.register_blueprint(records.bp, url_prefix='/api/records')
    app.register_blueprint(logs.bp, url_prefix='/api/logs')
    app.register_blueprint(roles.bp, url_prefix='/api/roles')
    app.register_blueprint(dept.bp, url_prefix='/api/dept')
    app.register_blueprint(menus.bp, url_prefix='/api/menus')


def register_handlers(app):
    from flask import jsonify

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'code': 404, 'msg': 'Not Found', 'data': None}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'code': 500, 'msg': 'Internal Server Error', 'data': None}), 500


def init_data():
    from app.models import SysUser, SysRole, SysMenu, SysUserRole, SysRoleMenu
    from app.utils.crypto import md5_encrypt
    import hashlib

    if not SysRole.query.filter_by(role_code='admin').first():
        admin_role = SysRole(
            role_name='超级管理员',
            role_code='admin',
            role_sort=1,
            status=0,
            remark='系统超级管理员'
        )
        db.session.add(admin_role)

        operator_role = SysRole(
            role_name='运营',
            role_code='operator',
            role_sort=2,
            status=0,
            remark='运营人员'
        )
        db.session.add(operator_role)

        guest_role = SysRole(
            role_name='访客',
            role_code='guest',
            role_sort=3,
            status=0,
            remark='只读访客'
        )
        db.session.add(guest_role)

        db.session.commit()

    if not SysUser.query.filter_by(username='admin').first():
        admin_role = SysRole.query.filter_by(role_code='admin').first()
        password_hash = hashlib.md5('123456'.encode()).hexdigest()
        admin_user = SysUser(
            username='admin',
            password=password_hash,
            nickname='管理员',
            status=0,
            remark='系统管理员'
        )
        db.session.add(admin_user)
        db.session.commit()

        user_role = SysUserRole(user_id=admin_user.user_id, role_id=admin_role.role_id)
        db.session.add(user_role)
        db.session.commit()

    if not SysMenu.query.filter_by(menu_name='仪表盘').first():
        menus = [
            {'menu_name': '仪表盘', 'menu_type': 'M', 'path': '/dashboard', 'component': 'dashboard/index', 'icon': 'Monitor', 'menu_sort': 1},
            {'menu_name': '系统管理', 'menu_type': 'M', 'path': '/system', 'icon': 'Setting', 'menu_sort': 2},
            {'menu_name': '文章管理', 'menu_type': 'M', 'path': '/article', 'icon': 'Document', 'menu_sort': 3},
            {'menu_name': '推广管理', 'menu_type': 'M', 'path': '/promotion', 'icon': 'Goods', 'menu_sort': 4},
            {'menu_name': 'AI配置', 'menu_type': 'M', 'path': '/ai-config', 'icon': 'MagicStick', 'menu_sort': 5},
        ]

        menu_id_map = {}
        for m in menus:
            menu = SysMenu(**m)
            db.session.add(menu)
            db.session.flush()
            menu_id_map[m['menu_name']] = menu.menu_id

        child_menus = [
            {'menu_name': '用户管理', 'menu_type': 'C', 'path': '/system/user', 'component': 'system/user/index', 'parent_id': menu_id_map['系统管理'], 'menu_sort': 1},
            {'menu_name': '角色管理', 'menu_type': 'C', 'path': '/system/role', 'component': 'system/role/index', 'parent_id': menu_id_map['系统管理'], 'menu_sort': 2},
            {'menu_name': '部门管理', 'menu_type': 'C', 'path': '/system/dept', 'component': 'system/dept/index', 'parent_id': menu_id_map['系统管理'], 'menu_sort': 3},
            {'menu_name': '登录日志', 'menu_type': 'C', 'path': '/system/login-log', 'component': 'system/login-log/index', 'parent_id': menu_id_map['系统管理'], 'menu_sort': 4},
            {'menu_name': '操作日志', 'menu_type': 'C', 'path': '/system/oper-log', 'component': 'system/oper-log/index', 'parent_id': menu_id_map['系统管理'], 'menu_sort': 5},
            {'menu_name': '文章发布', 'menu_type': 'C', 'path': '/article/publish', 'component': 'article/publish/index', 'parent_id': menu_id_map['文章管理'], 'menu_sort': 1},
            {'menu_name': '发布记录', 'menu_type': 'C', 'path': '/article/record', 'component': 'article/record/index', 'parent_id': menu_id_map['文章管理'], 'menu_sort': 2},
            {'menu_name': '产品管理', 'menu_type': 'C', 'path': '/promotion/product', 'component': 'promotion/product/index', 'parent_id': menu_id_map['推广管理'], 'menu_sort': 1},
            {'menu_name': '图片管理', 'menu_type': 'C', 'path': '/promotion/image', 'component': 'promotion/image/index', 'parent_id': menu_id_map['推广管理'], 'menu_sort': 2},
            {'menu_name': '网站配置', 'menu_type': 'C', 'path': '/promotion/website', 'component': 'promotion/website/index', 'parent_id': menu_id_map['推广管理'], 'menu_sort': 3},
            {'menu_name': '关键词管理', 'menu_type': 'C', 'path': '/ai-config/keyword', 'component': 'ai-config/keyword/index', 'parent_id': menu_id_map['AI配置'], 'menu_sort': 1},
            {'menu_name': 'AI模型', 'menu_type': 'C', 'path': '/ai-config/model', 'component': 'ai-config/model/index', 'parent_id': menu_id_map['AI配置'], 'menu_sort': 2},
            {'menu_name': '内容模板', 'menu_type': 'C', 'path': '/ai-config/content-template', 'component': 'ai-config/content-template/index', 'parent_id': menu_id_map['AI配置'], 'menu_sort': 3},
            {'menu_name': '标题模板', 'menu_type': 'C', 'path': '/ai-config/title-template', 'component': 'ai-config/title-template/index', 'parent_id': menu_id_map['AI配置'], 'menu_sort': 4},
        ]

        for m in child_menus:
            menu = SysMenu(**m)
            db.session.add(menu)
            db.session.flush()
            menu_id_map[m['menu_name']] = menu.menu_id

        button_menus = [
            {'menu_name': '用户新增', 'menu_type': 'F', 'perms': 'system:user:add', 'parent_id': menu_id_map['用户管理'], 'menu_sort': 1},
            {'menu_name': '用户编辑', 'menu_type': 'F', 'perms': 'system:user:edit', 'parent_id': menu_id_map['用户管理'], 'menu_sort': 2},
            {'menu_name': '用户删除', 'menu_type': 'F', 'perms': 'system:user:delete', 'parent_id': menu_id_map['用户管理'], 'menu_sort': 3},
            {'menu_name': '用户查询', 'menu_type': 'F', 'perms': 'system:user:query', 'parent_id': menu_id_map['用户管理'], 'menu_sort': 4},
            
            {'menu_name': '角色新增', 'menu_type': 'F', 'perms': 'system:role:add', 'parent_id': menu_id_map['角色管理'], 'menu_sort': 1},
            {'menu_name': '角色编辑', 'menu_type': 'F', 'perms': 'system:role:edit', 'parent_id': menu_id_map['角色管理'], 'menu_sort': 2},
            {'menu_name': '角色删除', 'menu_type': 'F', 'perms': 'system:role:delete', 'parent_id': menu_id_map['角色管理'], 'menu_sort': 3},
            {'menu_name': '角色查询', 'menu_type': 'F', 'perms': 'system:role:query', 'parent_id': menu_id_map['角色管理'], 'menu_sort': 4},
            
            {'menu_name': '部门新增', 'menu_type': 'F', 'perms': 'system:dept:add', 'parent_id': menu_id_map['部门管理'], 'menu_sort': 1},
            {'menu_name': '部门编辑', 'menu_type': 'F', 'perms': 'system:dept:edit', 'parent_id': menu_id_map['部门管理'], 'menu_sort': 2},
            {'menu_name': '部门删除', 'menu_type': 'F', 'perms': 'system:dept:delete', 'parent_id': menu_id_map['部门管理'], 'menu_sort': 3},
            {'menu_name': '部门查询', 'menu_type': 'F', 'perms': 'system:dept:query', 'parent_id': menu_id_map['部门管理'], 'menu_sort': 4},
            
            {'menu_name': '日志查询', 'menu_type': 'F', 'perms': 'system:loginlog:query', 'parent_id': menu_id_map['登录日志'], 'menu_sort': 1},
            
            {'menu_name': '日志查询', 'menu_type': 'F', 'perms': 'system:operlog:query', 'parent_id': menu_id_map['操作日志'], 'menu_sort': 1},
            
            {'menu_name': '文章发布', 'menu_type': 'F', 'perms': 'article:publish:add', 'parent_id': menu_id_map['文章发布'], 'menu_sort': 1},
            {'menu_name': '文章查询', 'menu_type': 'F', 'perms': 'article:publish:query', 'parent_id': menu_id_map['文章发布'], 'menu_sort': 2},
            
            {'menu_name': '记录查询', 'menu_type': 'F', 'perms': 'article:record:query', 'parent_id': menu_id_map['发布记录'], 'menu_sort': 1},
            {'menu_name': '记录删除', 'menu_type': 'F', 'perms': 'article:record:delete', 'parent_id': menu_id_map['发布记录'], 'menu_sort': 2},
            
            {'menu_name': '产品新增', 'menu_type': 'F', 'perms': 'promotion:product:add', 'parent_id': menu_id_map['产品管理'], 'menu_sort': 1},
            {'menu_name': '产品编辑', 'menu_type': 'F', 'perms': 'promotion:product:edit', 'parent_id': menu_id_map['产品管理'], 'menu_sort': 2},
            {'menu_name': '产品删除', 'menu_type': 'F', 'perms': 'promotion:product:delete', 'parent_id': menu_id_map['产品管理'], 'menu_sort': 3},
            {'menu_name': '产品查询', 'menu_type': 'F', 'perms': 'promotion:product:query', 'parent_id': menu_id_map['产品管理'], 'menu_sort': 4},
            
            {'menu_name': '图片上传', 'menu_type': 'F', 'perms': 'promotion:image:add', 'parent_id': menu_id_map['图片管理'], 'menu_sort': 1},
            {'menu_name': '图片删除', 'menu_type': 'F', 'perms': 'promotion:image:delete', 'parent_id': menu_id_map['图片管理'], 'menu_sort': 2},
            {'menu_name': '图片查询', 'menu_type': 'F', 'perms': 'promotion:image:query', 'parent_id': menu_id_map['图片管理'], 'menu_sort': 3},
            
            {'menu_name': '网站新增', 'menu_type': 'F', 'perms': 'promotion:website:add', 'parent_id': menu_id_map['网站配置'], 'menu_sort': 1},
            {'menu_name': '网站编辑', 'menu_type': 'F', 'perms': 'promotion:website:edit', 'parent_id': menu_id_map['网站配置'], 'menu_sort': 2},
            {'menu_name': '网站删除', 'menu_type': 'F', 'perms': 'promotion:website:delete', 'parent_id': menu_id_map['网站配置'], 'menu_sort': 3},
            {'menu_name': '网站查询', 'menu_type': 'F', 'perms': 'promotion:website:query', 'parent_id': menu_id_map['网站配置'], 'menu_sort': 4},
            
            {'menu_name': '关键词新增', 'menu_type': 'F', 'perms': 'ai:keyword:add', 'parent_id': menu_id_map['关键词管理'], 'menu_sort': 1},
            {'menu_name': '关键词编辑', 'menu_type': 'F', 'perms': 'ai:keyword:edit', 'parent_id': menu_id_map['关键词管理'], 'menu_sort': 2},
            {'menu_name': '关键词删除', 'menu_type': 'F', 'perms': 'ai:keyword:delete', 'parent_id': menu_id_map['关键词管理'], 'menu_sort': 3},
            {'menu_name': '关键词查询', 'menu_type': 'F', 'perms': 'ai:keyword:query', 'parent_id': menu_id_map['关键词管理'], 'menu_sort': 4},
            
            {'menu_name': '模型新增', 'menu_type': 'F', 'perms': 'ai:model:add', 'parent_id': menu_id_map['AI模型'], 'menu_sort': 1},
            {'menu_name': '模型编辑', 'menu_type': 'F', 'perms': 'ai:model:edit', 'parent_id': menu_id_map['AI模型'], 'menu_sort': 2},
            {'menu_name': '模型删除', 'menu_type': 'F', 'perms': 'ai:model:delete', 'parent_id': menu_id_map['AI模型'], 'menu_sort': 3},
            {'menu_name': '模型查询', 'menu_type': 'F', 'perms': 'ai:model:query', 'parent_id': menu_id_map['AI模型'], 'menu_sort': 4},
            
            {'menu_name': '模板新增', 'menu_type': 'F', 'perms': 'ai:content:add', 'parent_id': menu_id_map['内容模板'], 'menu_sort': 1},
            {'menu_name': '模板编辑', 'menu_type': 'F', 'perms': 'ai:content:edit', 'parent_id': menu_id_map['内容模板'], 'menu_sort': 2},
            {'menu_name': '模板删除', 'menu_type': 'F', 'perms': 'ai:content:delete', 'parent_id': menu_id_map['内容模板'], 'menu_sort': 3},
            {'menu_name': '模板查询', 'menu_type': 'F', 'perms': 'ai:content:query', 'parent_id': menu_id_map['内容模板'], 'menu_sort': 4},
            
            {'menu_name': '模板新增', 'menu_type': 'F', 'perms': 'ai:title:add', 'parent_id': menu_id_map['标题模板'], 'menu_sort': 1},
            {'menu_name': '模板编辑', 'menu_type': 'F', 'perms': 'ai:title:edit', 'parent_id': menu_id_map['标题模板'], 'menu_sort': 2},
            {'menu_name': '模板删除', 'menu_type': 'F', 'perms': 'ai:title:delete', 'parent_id': menu_id_map['标题模板'], 'menu_sort': 3},
            {'menu_name': '模板查询', 'menu_type': 'F', 'perms': 'ai:title:query', 'parent_id': menu_id_map['标题模板'], 'menu_sort': 4},
        ]

        for m in button_menus:
            menu = SysMenu(**m)
            db.session.add(menu)

        db.session.commit()

        admin_role = SysRole.query.filter_by(role_code='admin').first()
        for menu in SysMenu.query.all():
            role_menu = SysRoleMenu(role_id=admin_role.role_id, menu_id=menu.menu_id)
            db.session.add(role_menu)

        db.session.commit()