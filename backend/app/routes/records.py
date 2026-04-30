from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, PublishRecord, Website

bp = Blueprint('records', __name__)


@bp.route('', methods=['GET'])
@token_required
def get_records():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    website_id = request.args.get('websiteId', type=int)
    status = request.args.get('status', '')
    start_time = request.args.get('startTime', '')
    end_time = request.args.get('endTime', '')

    query = PublishRecord.query

    if website_id:
        query = query.filter(PublishRecord.website_id == website_id)
    if status:
        query = query.filter(PublishRecord.status == status)
    if start_time:
        query = query.filter(PublishRecord.create_time >= start_time)
    if end_time:
        query = query.filter(PublishRecord.create_time <= end_time)

    total = query.count()
    records = query.order_by(PublishRecord.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

    record_list = []
    for r in records:
        website = Website.query.get(r.website_id)
        record_list.append({
            'id': r.id,
            'productId': r.product_id,
            'websiteId': r.website_id,
            'websiteName': website.name if website else '',
            'title': r.title,
            'status': r.status,
            'resultUrl': r.result_url,
            'errorMsg': r.error_msg,
            'publishTime': r.publish_time.strftime('%Y-%m-%d %H:%M:%S') if r.publish_time else None,
            'createTime': r.create_time.strftime('%Y-%m-%d %H:%M:%S') if r.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': record_list, 'total': total, 'page': page, 'pageSize': page_size}})


@bp.route('/<int:record_id>', methods=['GET'])
@token_required
def get_record(record_id):
    record = PublishRecord.query.get(record_id)
    if not record:
        return jsonify({'code': 404, 'msg': '记录不存在', 'data': None})

    website = Website.query.get(record.website_id)

    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'id': record.id,
            'productId': record.product_id,
            'websiteId': record.website_id,
            'websiteName': website.name if website else '',
            'title': record.title,
            'content': record.content,
            'status': record.status,
            'resultUrl': record.result_url,
            'errorMsg': record.error_msg,
            'publishTime': record.publish_time.strftime('%Y-%m-%d %H:%M:%S') if record.publish_time else None,
            'createTime': record.create_time.strftime('%Y-%m-%d %H:%M:%S') if record.create_time else None
        }
    })


@bp.route('/<int:record_id>', methods=['DELETE'])
@token_required
def delete_record(record_id):
    record = PublishRecord.query.get(record_id)
    if not record:
        return jsonify({'code': 404, 'msg': '记录不存在', 'data': None})

    db.session.delete(record)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@bp.route('', methods=['DELETE'])
@token_required
def clear_records():
    PublishRecord.query.delete()
    db.session.commit()

    return jsonify({'code': 200, 'msg': '清空成功', 'data': None})
