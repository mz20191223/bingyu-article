from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, SysRole, SysRoleMenu, SysMenu

bp = Blueprint('roles', __name__)


@bp.route('', methods=['GET'])
@token_required
def get_roles():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)

    total = SysRole.query.count()
    roles = SysRole.query.offset((page - 1) * page_size).limit(page_size).all()

    role_list = []
    for r in roles:
        role_list.append({
            'roleId': r.role_id,
            'roleName': r.role_name,
            'roleCode': r.role_code,
            'roleSort': r.role_sort,
            'status': r.status,
            'remark': r.remark,
            'createTime': r.create_time.strftime('%Y-%m-%d %H:%M:%S') if r.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': role_list, 'total': total, 'page': page, 'pageSize': page_size}})


@bp.route('', methods=['POST'])
@token_required
def create_role():
    data = request.get_json()
    role_name = data.get('roleName')
    role_code = data.get('roleCode')

    if not role_name or not role_code:
        return jsonify({'code': 400, 'msg': '角色名称和编码不能为空', 'data': None})

    if SysRole.query.filter_by(role_code=role_code).first():
        return jsonify({'code': 400, 'msg': '角色编码已存在', 'data': None})

    role = SysRole(
        role_name=role_name,
        role_code=role_code,
        role_sort=data.get('roleSort', 0),
        status=data.get('status', 0),
        remark=data.get('remark')
    )
    db.session.add(role)
    db.session.commit()

    menu_ids = data.get('menuIds', [])
    for menu_id in menu_ids:
        role_menu = SysRoleMenu(role_id=role.role_id, menu_id=menu_id)
        db.session.add(role_menu)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@bp.route('/<int:role_id>', methods=['PUT'])
@token_required
def update_role(role_id):
    role = SysRole.query.get(role_id)
    if not role:
        return jsonify({'code': 404, 'msg': '角色不存在', 'data': None})

    data = request.get_json()
    if 'roleName' in data:
        role.role_name = data['roleName']
    if 'roleSort' in data:
        role.role_sort = data['roleSort']
    if 'status' in data:
        role.status = data['status']
    if 'remark' in data:
        role.remark = data['remark']

    db.session.commit()

    menu_ids = data.get('menuIds', [])
    SysRoleMenu.query.filter_by(role_id=role_id).delete()
    for menu_id in menu_ids:
        role_menu = SysRoleMenu(role_id=role_id, menu_id=menu_id)
        db.session.add(role_menu)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@bp.route('/<int:role_id>', methods=['DELETE'])
@token_required
def delete_role(role_id):
    role = SysRole.query.get(role_id)
    if not role:
        return jsonify({'code': 404, 'msg': '角色不存在', 'data': None})

    SysRoleMenu.query.filter_by(role_id=role_id).delete()
    db.session.delete(role)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@bp.route('/<int:role_id>/menus', methods=['GET'])
@token_required
def get_role_menus(role_id):
    role_menus = SysRoleMenu.query.filter_by(role_id=role_id).all()
    menu_ids = [rm.menu_id for rm in role_menus]
    return jsonify({'code': 200, 'msg': 'success', 'data': menu_ids})