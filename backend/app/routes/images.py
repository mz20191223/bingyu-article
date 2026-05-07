from flask import Blueprint, request, jsonify, g, send_from_directory
from app.routes.auth import token_required
from app.models import db, Image, Product, SysOperLog
from werkzeug.utils import secure_filename
from datetime import datetime
import os

bp = Blueprint('images', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# 获取 backend 目录路径 (routes/images.py -> app -> backend)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'uploads')

@bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_uploads(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['POST'])
@token_required
def upload_image():
    if 'file' not in request.files:
        return jsonify({'code': 400, 'msg': '没有文件', 'data': None})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'msg': '文件名为空', 'data': None})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = int(datetime.now().timestamp())
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        try:
            file.save(filepath)
        except Exception as e:
            return jsonify({'code': 500, 'msg': f'保存文件失败: {str(e)}', 'data': None})

        file_url = f'/api/images/uploads/{filename}'
        return jsonify({'code': 200, 'msg': '上传成功', 'data': {'url': file_url}})

    return jsonify({'code': 400, 'msg': '不支持的文件类型', 'data': None})


@bp.route('', methods=['GET'])
@token_required
def get_images():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    product_id = request.args.get('productId', type=int)
    status = request.args.get('status', type=int)

    query = Image.query

    if product_id:
        query = query.filter(Image.products.any(id=product_id))
    if status is not None:
        query = query.filter(Image.status == status)

    total = query.count()
    images = query.offset((page - 1) * page_size).limit(page_size).all()

    image_list = []
    for img in images:
        products = [{
            'id': p.id,
            'name': p.name
        } for p in img.products]
        image_list.append({
            'id': img.id,
            'url': img.url,
            'positionType': img.position_type,
            'positionValue': img.position_value,
            'positionMode': img.position_mode,
            'products': products,
            'status': img.status,
            'createTime': img.create_time.strftime('%Y-%m-%d %H:%M:%S') if img.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': image_list, 'total': total, 'page': page, 'pageSize': page_size}})


@bp.route('', methods=['POST'])
@token_required
def create_image():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'code': 400, 'msg': '图片URL不能为空', 'data': None})

    image = Image(
        url=url,
        position_type=data.get('positionType', 'auto'),
        position_value=data.get('positionValue'),
        position_mode=data.get('positionMode', 'before'),
        status=data.get('status', 1)
    )
    
    product_ids = data.get('productIds', [])
    for product_id in product_ids:
        product = Product.query.get(product_id)
        if product:
            image.products.append(product)
    
    db.session.add(image)
    db.session.commit()

    log = SysOperLog(title='图片管理', business_type=1, oper_name=g.username, oper_url='/api/images', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@bp.route('/<int:image_id>', methods=['PUT'])
@token_required
def update_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'code': 404, 'msg': '图片不存在', 'data': None})

    data = request.get_json()
    if 'url' in data:
        image.url = data['url']
    if 'positionType' in data:
        image.position_type = data['positionType']
    if 'positionValue' in data:
        image.position_value = data['positionValue']
    if 'positionMode' in data:
        image.position_mode = data['positionMode']
    if 'status' in data:
        image.status = data['status']
    
    if 'productIds' in data:
        image.products.clear()
        product_ids = data['productIds']
        for product_id in product_ids:
            product = Product.query.get(product_id)
            if product:
                image.products.append(product)

    db.session.commit()

    log = SysOperLog(title='图片管理', business_type=2, oper_name=g.username, oper_url=f'/api/images/{image_id}', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@bp.route('/<int:image_id>', methods=['DELETE'])
@token_required
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'code': 404, 'msg': '图片不存在', 'data': None})

    db.session.delete(image)
    db.session.commit()

    log = SysOperLog(title='图片管理', business_type=3, oper_name=g.username, oper_url=f'/api/images/{image_id}', status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@bp.route('/<int:image_id>/status', methods=['PUT'])
@token_required
def update_image_status(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({'code': 404, 'msg': '图片不存在', 'data': None})

    data = request.get_json()
    image.status = data.get('status', 1)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '状态更新成功', 'data': None})


