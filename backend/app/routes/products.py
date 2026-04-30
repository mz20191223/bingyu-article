from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, Product, SysOperLog

bp = Blueprint('products', __name__)


@bp.route('', methods=['GET'])
@token_required
def get_products():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    name = request.args.get('name', '')
    status = request.args.get('status', type=int)

    query = Product.query

    if name:
        query = query.filter(Product.name.like(f'%{name}%'))
    if status is not None:
        query = query.filter(Product.status == status)

    total = query.count()
    products = query.offset((page - 1) * page_size).limit(page_size).all()

    product_list = []
    for p in products:
        product_list.append({
            'id': p.id,
            'name': p.name,
            'url': p.url,
            'status': p.status,
            'createTime': p.create_time.strftime('%Y-%m-%d %H:%M:%S') if p.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': product_list, 'total': total, 'page': page, 'pageSize': page_size}})


@bp.route('/<int:product_id>', methods=['GET'])
@token_required
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'msg': '产品不存在', 'data': None})

    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'id': product.id,
            'name': product.name,
            'url': product.url,
            'status': product.status
        }
    })


@bp.route('', methods=['POST'])
@token_required
def create_product():
    data = request.get_json()
    name = data.get('name')
    url = data.get('url')

    if not name:
        return jsonify({'code': 400, 'msg': '产品名称不能为空', 'data': None})

    product = Product(name=name, url=url, status=data.get('status', 1))
    db.session.add(product)
    db.session.commit()

    log = SysOperLog(title='产品管理', business_type=1, oper_name=g.username, oper_url='/api/products', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@bp.route('/<int:product_id>', methods=['PUT'])
@token_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'msg': '产品不存在', 'data': None})

    data = request.get_json()
    if 'name' in data:
        product.name = data['name']
    if 'url' in data:
        product.url = data['url']
    if 'status' in data:
        product.status = data['status']

    db.session.commit()

    log = SysOperLog(title='产品管理', business_type=2, oper_name=g.username, oper_url=f'/api/products/{product_id}', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@bp.route('/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'msg': '产品不存在', 'data': None})

    db.session.delete(product)
    db.session.commit()

    log = SysOperLog(title='产品管理', business_type=3, oper_name=g.username, oper_url=f'/api/products/{product_id}', status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@bp.route('/<int:product_id>/status', methods=['PUT'])
@token_required
def update_product_status(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'msg': '产品不存在', 'data': None})

    data = request.get_json()
    product.status = data.get('status', 1)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '状态更新成功', 'data': None})