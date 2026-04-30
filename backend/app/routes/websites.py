from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, Website, SysOperLog

bp = Blueprint('websites', __name__)


@bp.route('', methods=['GET'])
@token_required
def get_websites():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    status = request.args.get('status', type=int)

    query = Website.query

    if status is not None:
        query = query.filter(Website.status == status)

    total = query.count()
    websites = query.offset((page - 1) * page_size).limit(page_size).all()

    website_list = []
    for w in websites:
        website_list.append({
            'id': w.id,
            'name': w.name,
            'code': w.code,
            'loginUrl': w.login_url,
            'publishUrl': w.publish_url,
            'cookie': '***' if w.cookie else '',
            'status': w.status,
            'createTime': w.create_time.strftime('%Y-%m-%d %H:%M:%S') if w.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': website_list, 'total': total, 'page': page, 'pageSize': page_size}})


@bp.route('/<int:website_id>', methods=['GET'])
@token_required
def get_website(website_id):
    website = Website.query.get(website_id)
    if not website:
        return jsonify({'code': 404, 'msg': '网站不存在', 'data': None})

    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'id': website.id,
            'name': website.name,
            'code': website.code,
            'loginUrl': website.login_url,
            'publishUrl': website.publish_url,
            'cookie': website.cookie,
            'status': website.status
        }
    })


@bp.route('', methods=['POST'])
@token_required
def create_website():
    data = request.get_json()
    name = data.get('name')
    code = data.get('code')
    login_url = data.get('loginUrl')

    if not name or not code or not login_url:
        return jsonify({'code': 400, 'msg': '必填项不能为空', 'data': None})

    if Website.query.filter_by(code=code).first():
        return jsonify({'code': 400, 'msg': '网站标识已存在', 'data': None})

    website = Website(
        name=name,
        code=code,
        login_url=login_url,
        publish_url=data.get('publishUrl'),
        cookie=data.get('cookie'),
        status=data.get('status', 1)
    )
    db.session.add(website)
    db.session.commit()

    log = SysOperLog(title='网站配置', business_type=1, oper_name=g.username, oper_url='/api/websites', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@bp.route('/<int:website_id>', methods=['PUT'])
@token_required
def update_website(website_id):
    website = Website.query.get(website_id)
    if not website:
        return jsonify({'code': 404, 'msg': '网站不存在', 'data': None})

    data = request.get_json()
    if 'name' in data:
        website.name = data['name']
    if 'loginUrl' in data:
        website.login_url = data['loginUrl']
    if 'publishUrl' in data:
        website.publish_url = data['publishUrl']
    if 'cookie' in data:
        website.cookie = data['cookie']
    if 'status' in data:
        website.status = data['status']

    db.session.commit()

    log = SysOperLog(title='网站配置', business_type=2, oper_name=g.username, oper_url=f'/api/websites/{website_id}', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@bp.route('/<int:website_id>', methods=['DELETE'])
@token_required
def delete_website(website_id):
    website = Website.query.get(website_id)
    if not website:
        return jsonify({'code': 404, 'msg': '网站不存在', 'data': None})

    db.session.delete(website)
    db.session.commit()

    log = SysOperLog(title='网站配置', business_type=3, oper_name=g.username, oper_url=f'/api/websites/{website_id}', status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})