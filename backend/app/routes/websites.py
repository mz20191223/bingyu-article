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
            'username': w.username,
            'password': '***' if w.password else '',
            'cookie': '***' if w.cookie else '',
            'usernameSelector': w.username_selector,
            'passwordSelector': w.password_selector,
            'loginButtonSelector': w.login_button_selector,
            'titleSelector': w.title_selector,
            'contentSelector': w.content_selector,
            'categorySelector': w.category_selector,
            'publishButtonSelector': w.publish_button_selector,
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
            'username': website.username,
            'password': website.password,
            'cookie': website.cookie,
            'usernameSelector': website.username_selector,
            'passwordSelector': website.password_selector,
            'loginButtonSelector': website.login_button_selector,
            'titleSelector': website.title_selector,
            'contentSelector': website.content_selector,
            'categorySelector': website.category_selector,
            'publishButtonSelector': website.publish_button_selector,
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

    if not name or not code:
        return jsonify({'code': 400, 'msg': '网站名称和标识不能为空', 'data': None})

    if Website.query.filter_by(code=code).first():
        return jsonify({'code': 400, 'msg': '网站标识已存在', 'data': None})

    website = Website(
        name=name,
        code=code,
        login_url=data.get('loginUrl'),
        publish_url=data.get('publishUrl'),
        username=data.get('username'),
        password=data.get('password'),
        cookie=data.get('cookie'),
        username_selector=data.get('usernameSelector'),
        password_selector=data.get('passwordSelector'),
        login_button_selector=data.get('loginButtonSelector'),
        title_selector=data.get('titleSelector'),
        content_selector=data.get('contentSelector'),
        category_selector=data.get('categorySelector'),
        publish_button_selector=data.get('publishButtonSelector'),
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
    if 'username' in data:
        website.username = data['username']
    if 'password' in data:
        website.password = data['password']
    if 'cookie' in data:
        website.cookie = data['cookie']
    if 'usernameSelector' in data:
        website.username_selector = data['usernameSelector']
    if 'passwordSelector' in data:
        website.password_selector = data['passwordSelector']
    if 'loginButtonSelector' in data:
        website.login_button_selector = data['loginButtonSelector']
    if 'titleSelector' in data:
        website.title_selector = data['titleSelector']
    if 'contentSelector' in data:
        website.content_selector = data['contentSelector']
    if 'categorySelector' in data:
        website.category_selector = data['categorySelector']
    if 'publishButtonSelector' in data:
        website.publish_button_selector = data['publishButtonSelector']
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