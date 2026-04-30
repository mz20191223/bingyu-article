from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, Keyword, SysOperLog

bp = Blueprint('keywords', __name__)


@bp.route('', methods=['GET'])
@token_required
def get_keywords():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    status = request.args.get('status', type=int)

    query = Keyword.query

    if status is not None:
        query = query.filter(Keyword.status == status)

    total = query.count()
    keywords = query.offset((page - 1) * page_size).limit(page_size).all()

    keyword_list = []
    for kw in keywords:
        keyword_list.append({
            'id': kw.id,
            'keyword': kw.keyword,
            'status': kw.status,
            'createTime': kw.create_time.strftime('%Y-%m-%d %H:%M:%S') if kw.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': keyword_list, 'total': total, 'page': page, 'pageSize': page_size}})


@bp.route('', methods=['POST'])
@token_required
def create_keyword():
    data = request.get_json()
    keyword = data.get('keyword')

    if not keyword:
        return jsonify({'code': 400, 'msg': '关键词不能为空', 'data': None})

    if Keyword.query.filter_by(keyword=keyword).first():
        return jsonify({'code': 400, 'msg': '关键词已存在', 'data': None})

    kw = Keyword(keyword=keyword, status=data.get('status', 1))
    db.session.add(kw)
    db.session.commit()

    log = SysOperLog(title='关键词管理', business_type=1, oper_name=g.username, oper_url='/api/keywords', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@bp.route('/<int:keyword_id>', methods=['PUT'])
@token_required
def update_keyword(keyword_id):
    keyword = Keyword.query.get(keyword_id)
    if not keyword:
        return jsonify({'code': 404, 'msg': '关键词不存在', 'data': None})

    data = request.get_json()
    if 'keyword' in data:
        keyword.keyword = data['keyword']
    if 'status' in data:
        keyword.status = data['status']

    db.session.commit()

    log = SysOperLog(title='关键词管理', business_type=2, oper_name=g.username, oper_url=f'/api/keywords/{keyword_id}', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@bp.route('/<int:keyword_id>', methods=['DELETE'])
@token_required
def delete_keyword(keyword_id):
    keyword = Keyword.query.get(keyword_id)
    if not keyword:
        return jsonify({'code': 404, 'msg': '关键词不存在', 'data': None})

    db.session.delete(keyword)
    db.session.commit()

    log = SysOperLog(title='关键词管理', business_type=3, oper_name=g.username, oper_url=f'/api/keywords/{keyword_id}', status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@bp.route('/<int:keyword_id>/status', methods=['PUT'])
@token_required
def update_keyword_status(keyword_id):
    keyword = Keyword.query.get(keyword_id)
    if not keyword:
        return jsonify({'code': 404, 'msg': '关键词不存在', 'data': None})

    data = request.get_json()
    keyword.status = data.get('status', 1)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '状态更新成功', 'data': None})


@bp.route('/import', methods=['POST'])
@token_required
def import_keywords():
    if 'file' not in request.files:
        return jsonify({'code': 400, 'msg': '请上传文件', 'data': None})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'msg': '请选择文件', 'data': None})

    try:
        import openpyxl
        wb = openpyxl.load_workbook(file)
        ws = wb.active
        keywords = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] and isinstance(row[0], str):
                keyword = row[0].strip()
                if keyword and not Keyword.query.filter_by(keyword=keyword).first():
                    kw = Keyword(keyword=keyword, status=1)
                    keywords.append(kw)

        db.session.add_all(keywords)
        db.session.commit()

        log = SysOperLog(title='关键词管理', business_type=1, oper_name=g.username, oper_url='/api/keywords/import', oper_param=f'导入{len(keywords)}个关键词', status=0)
        db.session.add(log)
        db.session.commit()

        return jsonify({'code': 200, 'msg': f'成功导入{len(keywords)}个关键词', 'data': {'count': len(keywords)}})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'导入失败: {str(e)}', 'data': None})