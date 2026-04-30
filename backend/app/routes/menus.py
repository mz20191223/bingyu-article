from flask import Blueprint, request, jsonify
from app.routes.auth import token_required
from app.models import SysMenu

bp = Blueprint('menus', __name__)


def menu_to_dict(menu):
    return {
        'menuId': menu.menu_id,
        'menuName': menu.menu_name,
        'parentId': menu.parent_id,
        'orderNum': menu.order_num,
        'menuSort': menu.menu_sort,
        'path': menu.path,
        'component': menu.component,
        'isFrame': menu.is_frame,
        'menuType': menu.menu_type,
        'visible': menu.visible,
        'status': menu.status,
        'perms': menu.perms,
        'icon': menu.icon,
        'children': []
    }


@bp.route('/tree', methods=['GET'])
@token_required
def get_menu_tree():
    menus = SysMenu.query.filter_by(status='0').order_by(SysMenu.order_num).all()
    menu_dict = {}
    
    for menu in menus:
        menu_dict[menu.menu_id] = menu_to_dict(menu)
    
    tree = []
    for menu_id, menu_data in menu_dict.items():
        if menu_data['parentId'] == 0:
            tree.append(menu_data)
        else:
            parent = menu_dict.get(menu_data['parentId'])
            if parent:
                parent['children'].append(menu_data)
    
    return jsonify({'code': 200, 'msg': 'success', 'data': tree})


@bp.route('', methods=['GET'])
@token_required
def get_menus():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    
    total = SysMenu.query.count()
    menus = SysMenu.query.offset((page - 1) * page_size).limit(page_size).all()
    
    menu_list = []
    for menu in menus:
        menu_list.append(menu_to_dict(menu))
    
    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': menu_list, 'total': total}})