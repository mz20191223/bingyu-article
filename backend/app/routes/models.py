from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, AIModel, SysOperLog

bp = Blueprint('models', __name__)


@bp.route('', methods=['GET'])
@token_required
def get_models():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    provider = request.args.get('provider', '')
    status = request.args.get('status', type=int)

    query = AIModel.query

    if provider:
        query = query.filter(AIModel.provider == provider)
    if status is not None:
        query = query.filter(AIModel.status == status)

    total = query.count()
    models = query.offset((page - 1) * page_size).limit(page_size).all()

    model_list = []
    for m in models:
        model_list.append({
            'id': m.id,
            'name': m.name,
            'provider': m.provider,
            'apiKey': m.api_key[:10] + '***' if m.api_key else '',
            'apiUrl': m.api_url,
            'modelName': m.model_name,
            'parameters': m.parameters,
            'isDefault': m.is_default,
            'status': m.status,
            'createTime': m.create_time.strftime('%Y-%m-%d %H:%M:%S') if m.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': model_list, 'total': total, 'page': page, 'pageSize': page_size}})


@bp.route('', methods=['POST'])
@token_required
def create_model():
    data = request.get_json()
    name = data.get('name')
    provider = data.get('provider')
    api_key = data.get('apiKey')
    api_url = data.get('apiUrl')

    if not name or not provider or not api_key or not api_url:
        return jsonify({'code': 400, 'msg': '必填项不能为空', 'data': None})

    model = AIModel(
        name=name,
        provider=provider,
        api_key=api_key,
        api_url=api_url,
        model_name=data.get('modelName'),
        parameters=data.get('parameters'),
        is_default=data.get('isDefault', 0),
        status=data.get('status', 1),
        create_by=g.user_id
    )
    db.session.add(model)
    db.session.commit()

    log = SysOperLog(title='AI模型配置', business_type=1, oper_name=g.username, oper_url='/api/models', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@bp.route('/<int:model_id>', methods=['PUT'])
@token_required
def update_model(model_id):
    model = AIModel.query.get(model_id)
    if not model:
        return jsonify({'code': 404, 'msg': '模型不存在', 'data': None})

    data = request.get_json()
    if 'name' in data:
        model.name = data['name']
    if 'provider' in data:
        model.provider = data['provider']
    if 'apiKey' in data:
        model.api_key = data['apiKey']
    if 'apiUrl' in data:
        model.api_url = data['apiUrl']
    if 'modelName' in data:
        model.model_name = data['modelName']
    if 'parameters' in data:
        model.parameters = data['parameters']
    if 'status' in data:
        model.status = data['status']

    db.session.commit()

    log = SysOperLog(title='AI模型配置', business_type=2, oper_name=g.username, oper_url=f'/api/models/{model_id}', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@bp.route('/<int:model_id>', methods=['DELETE'])
@token_required
def delete_model(model_id):
    model = AIModel.query.get(model_id)
    if not model:
        return jsonify({'code': 404, 'msg': '模型不存在', 'data': None})

    db.session.delete(model)
    db.session.commit()

    log = SysOperLog(title='AI模型配置', business_type=3, oper_name=g.username, oper_url=f'/api/models/{model_id}', status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@bp.route('/<int:model_id>/default', methods=['PUT'])
@token_required
def set_default(model_id):
    model = AIModel.query.get(model_id)
    if not model:
        return jsonify({'code': 404, 'msg': '模型不存在', 'data': None})

    AIModel.query.update({'is_default': 0})
    model.is_default = 1
    db.session.commit()

    return jsonify({'code': 200, 'msg': '设置成功', 'data': None})
