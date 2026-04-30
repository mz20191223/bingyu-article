from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, SysUser, SysUserRole, SysRole, SysOperLog, SysMenu, SysRoleMenu, SysDept
from app.utils.crypto import md5_encrypt

bp = Blueprint('users', __name__)


@bp.route('/menu', methods=['GET'])
@token_required
def get_user_menu():
    user_id = g.user_id
    
    user_roles = SysUserRole.query.filter_by(user_id=user_id).all()
    role_ids = [ur.role_id for ur in user_roles]
    
    role_menus = SysRoleMenu.query.filter(SysRoleMenu.role_id.in_(role_ids)).all()
    menu_ids = [rm.menu_id for rm in role_menus]
    
    menus = SysMenu.query.filter(SysMenu.menu_id.in_(menu_ids)).all()
    
    menu_list = []
    for menu in menus:
        menu_list.append({
            'menuId': menu.menu_id,
            'menuName': menu.menu_name,
            'menuType': menu.menu_type,
            'path': menu.path,
            'component': menu.component,
            'parentId': menu.parent_id,
            'icon': menu.icon,
            'menuSort': menu.menu_sort,
            'status': menu.status
        })
    
    return jsonify({'code': 200, 'msg': 'success', 'data': menu_list})


@bp.route('', methods=['GET'])
@token_required
def get_users():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    username = request.args.get('username', '')
    status = request.args.get('status', type=int)

    query = SysUser.query

    if username:
        query = query.filter(SysUser.username.like(f'%{username}%'))
    if status is not None:
        query = query.filter(SysUser.status == status)

    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()

    user_list = []
    for user in users:
        dept = SysDept.query.get(user.dept_id) if user.dept_id else None
        user_list.append({
            'userId': user.user_id,
            'username': user.username,
            'nickname': user.nickname,
            'deptId': user.dept_id,
            'deptName': dept.dept_name if dept else '',
            'phone': user.phone,
            'email': user.email,
            'status': user.status,
            'createTime': user.create_time.strftime('%Y-%m-%d %H:%M:%S') if user.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': user_list, 'total': total, 'page': page, 'pageSize': page_size}})


@bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = SysUser.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在', 'data': None})

    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'userId': user.user_id,
            'username': user.username,
            'nickname': user.nickname,
            'phone': user.phone,
            'email': user.email,
            'status': user.status,
            'remark': user.remark
        }
    })


@bp.route('', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code': 400, 'msg': '用户名和密码不能为空', 'data': None})

    if SysUser.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'msg': '用户名已存在', 'data': None})

    user = SysUser(
        username=username,
        password=md5_encrypt(password),
        nickname=data.get('nickname'),
        dept_id=data.get('deptId'),
        phone=data.get('phone'),
        email=data.get('email'),
        status=data.get('status', 0),
        remark=data.get('remark')
    )
    db.session.add(user)
    db.session.commit()

    log = SysOperLog(
        title='用户管理',
        business_type=1,
        oper_name=g.username,
        oper_url='/api/users',
        oper_param=str(data),
        status=0
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    user = SysUser.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在', 'data': None})

    data = request.get_json()
    if 'nickname' in data:
        user.nickname = data['nickname']
    if 'deptId' in data:
        user.dept_id = data['deptId']
    if 'phone' in data:
        user.phone = data['phone']
    if 'email' in data:
        user.email = data['email']
    if 'status' in data:
        user.status = data['status']
    if 'remark' in data:
        user.remark = data['remark']

    db.session.commit()

    log = SysOperLog(
        title='用户管理',
        business_type=2,
        oper_name=g.username,
        oper_url=f'/api/users/{user_id}',
        oper_param=str(data),
        status=0
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    user = SysUser.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在', 'data': None})

    user.status = 1
    db.session.commit()

    log = SysOperLog(
        title='用户管理',
        business_type=3,
        oper_name=g.username,
        oper_url=f'/api/users/{user_id}',
        status=0
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@bp.route('/<int:user_id>/password', methods=['PUT'])
@token_required
def change_password(user_id):
    user = SysUser.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在', 'data': None})

    data = request.get_json()
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    if not old_password or not new_password:
        return jsonify({'code': 400, 'msg': '密码不能为空', 'data': None})

    if user.password != md5_encrypt(old_password):
        return jsonify({'code': 400, 'msg': '原密码错误', 'data': None})

    user.password = md5_encrypt(new_password)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '密码修改成功', 'data': None})
