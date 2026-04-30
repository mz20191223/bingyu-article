from flask import Blueprint, request, jsonify
from app.routes.auth import token_required
from app.models import SysDept
from app import db

bp = Blueprint('dept', __name__)


def dept_to_dict(dept):
    return {
        'deptId': dept.dept_id,
        'deptName': dept.dept_name,
        'parentId': dept.parent_id,
        'deptSort': dept.dept_sort,
        'leader': dept.leader,
        'phone': dept.phone,
        'email': dept.email,
        'status': dept.status,
        'createTime': dept.create_time.strftime('%Y-%m-%d %H:%M:%S') if dept.create_time else None
    }


@bp.route('/', methods=['GET'])
@token_required
def get_dept_list():
    depts = SysDept.query.all()
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': [dept_to_dict(dept) for dept in depts]
    })


@bp.route('/all', methods=['GET'])
@token_required
def get_all_depts():
    depts = SysDept.query.all()
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': [dept_to_dict(dept) for dept in depts]
    })


@bp.route('/', methods=['POST'])
@token_required
def add_dept():
    data = request.get_json()
    dept = SysDept(
        dept_name=data.get('deptName'),
        parent_id=data.get('parentId', 0),
        dept_sort=data.get('deptSort', 0),
        status=data.get('status', 1)
    )
    db.session.add(dept)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '添加成功', 'data': dept_to_dict(dept)})


@bp.route('/<int:dept_id>', methods=['PUT'])
@token_required
def update_dept(dept_id):
    data = request.get_json()
    dept = SysDept.query.get(dept_id)
    if not dept:
        return jsonify({'code': 404, 'msg': '部门不存在'})
    dept.dept_name = data.get('deptName', dept.dept_name)
    dept.parent_id = data.get('parentId', dept.parent_id)
    dept.dept_sort = data.get('deptSort', dept.dept_sort)
    dept.status = data.get('status', dept.status)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '更新成功', 'data': dept_to_dict(dept)})


@bp.route('/<int:dept_id>', methods=['DELETE'])
@token_required
def delete_dept(dept_id):
    dept = SysDept.query.get(dept_id)
    if not dept:
        return jsonify({'code': 404, 'msg': '部门不存在'})
    db.session.delete(dept)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})