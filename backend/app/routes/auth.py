import os
import sys
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, g, current_app
from functools import wraps
from app.models import db, SysUser, SysUserRole, SysRole, SysRoleMenu, SysMenu, SysLoginLog

bp = Blueprint('auth', __name__)

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-2024')


def generate_token(user_id, username, role_code):
    payload = {
        'user_id': user_id,
        'username': username,
        'role_code': role_code,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_app.logger.info(f'Token required check for {request.path}')
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                current_app.logger.error('Token split failed')
                return jsonify({'code': 401, 'msg': 'Token无效', 'data': None}), 401

        if not token:
            current_app.logger.error('No token provided')
            return jsonify({'code': 401, 'msg': '缺少Token', 'data': None}), 401

        payload = verify_token(token)
        if not payload:
            current_app.logger.error('Token verification failed')
            return jsonify({'code': 401, 'msg': 'Token已过期或无效', 'data': None}), 401

        g.user_id = payload.get('user_id')
        g.username = payload.get('username')
        g.role_code = payload.get('role_code')
        current_app.logger.info(f'Token OK for user {g.user_id}')

        return f(*args, **kwargs)

    return decorated


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code': 400, 'msg': '用户名和密码不能为空', 'data': None})

    import re
    if re.match(r'^[a-fA-F0-9]{32}$', password):
        password_hash = password
    else:
        from app.utils.crypto import md5_encrypt
        password_hash = md5_encrypt(password)

    user = SysUser.query.filter_by(username=username, password=password_hash).first()

    if not user:
        login_log = SysLoginLog(user_name=username, ipaddr=request.remote_addr, status='1', msg='用户名或密码错误')
        db.session.add(login_log)
        db.session.commit()
        return jsonify({'code': 400, 'msg': '用户名或密码错误', 'data': None})

    if user.status == 1:
        login_log = SysLoginLog(user_name=username, ipaddr=request.remote_addr, status='1', msg='账号已被禁用')
        db.session.add(login_log)
        db.session.commit()
        return jsonify({'code': 400, 'msg': '账号已被禁用', 'data': None})

    user_roles = SysUserRole.query.filter_by(user_id=user.user_id).all()
    role_ids = [ur.role_id for ur in user_roles]
    role = SysRole.query.filter_by(role_id=role_ids[0]).first() if role_ids else None
    role_code = role.role_code if role else 'guest'

    token = generate_token(user.user_id, user.username, role_code)

    login_log = SysLoginLog(user_name=username, ipaddr=request.remote_addr, status='0', msg='登录成功')
    db.session.add(login_log)
    db.session.commit()

    return jsonify({
        'code': 200,
        'msg': '登录成功',
        'data': {
            'token': token,
            'userInfo': {
                'userId': user.user_id,
                'username': user.username,
                'nickname': user.nickname,
                'role': role_code,
                'avatar': user.avatar
            }
        }
    })


@bp.route('/logout', methods=['POST'])
@token_required
def logout():
    return jsonify({'code': 200, 'msg': '退出成功', 'data': None})


@bp.route('/info', methods=['GET'])
@token_required
def get_user_info():
    user = SysUser.query.get(g.user_id)
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在', 'data': None})

    user_roles = SysUserRole.query.filter_by(user_id=user.user_id).all()
    role_ids = [ur.role_id for ur in user_roles]
    role = SysRole.query.filter_by(role_id=role_ids[0]).first() if role_ids else None
    role_code = role.role_code if role else 'guest'

    menus = []
    permissions = []
    
    if role_code == 'admin':
        all_menus = SysMenu.query.filter_by(status='0').order_by(SysMenu.menu_sort).all()
    else:
        menu_ids = SysRoleMenu.query.filter(SysRoleMenu.role_id.in_(role_ids)).all()
        mids = [m.menu_id for m in menu_ids]
        all_menus = SysMenu.query.filter(SysMenu.menu_id.in_(mids), SysMenu.status == '0').order_by(SysMenu.menu_sort).all()

    for menu in all_menus:
        menus.append({
            'menuId': menu.menu_id,
            'menuName': menu.menu_name,
            'parentId': menu.parent_id,
            'path': menu.path,
            'component': menu.component,
            'icon': menu.icon,
            'menuType': menu.menu_type
        })
        
        if menu.perms:
            permissions.append(menu.perms)

    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'userId': user.user_id,
            'username': user.username,
            'nickname': user.nickname,
            'role': role_code,
            'avatar': user.avatar,
            'menus': menus,
            'permissions': permissions
        }
    })