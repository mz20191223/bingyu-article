from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, PromptTemplate, Product, SysOperLog

prompt_bp = Blueprint('prompt_templates', __name__)


@prompt_bp.route('', methods=['GET'])
@token_required
def get_prompt_templates():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    status = request.args.get('status', type=int)

    query = PromptTemplate.query

    if status is not None:
        query = query.filter(PromptTemplate.status == status)

    total = query.count()
    templates = query.offset((page - 1) * page_size).limit(page_size).all()

    template_list = []
    for t in templates:
        product_ids = [p.id for p in t.products]
        product_names = [p.name for p in t.products]

        template_list.append({
            'id': t.id,
            'name': t.name,
            'productIds': product_ids,
            'productNames': product_names,
            'promptContent': t.prompt_content,
            'requiredParagraphs': t.required_paragraphs,
            'businessType': t.business_type,
            'isDefault': t.is_default,
            'status': t.status,
            'createTime': t.create_time.strftime('%Y-%m-%d %H:%M:%S') if t.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': template_list, 'total': total, 'page': page, 'pageSize': page_size}})


@prompt_bp.route('', methods=['POST'])
@token_required
def create_prompt_template():
    data = request.get_json()
    name = data.get('name')
    prompt_content = data.get('promptContent')

    if not name or not prompt_content:
        return jsonify({'code': 400, 'msg': '模板名称和提示词内容不能为空', 'data': None})

    template = PromptTemplate(
        name=name,
        prompt_content=prompt_content,
        required_paragraphs=data.get('requiredParagraphs', 5),
        business_type=data.get('businessType'),
        is_default=data.get('isDefault', 0),
        status=data.get('status', 1)
    )
    db.session.add(template)
    db.session.commit()

    product_ids = data.get('productIds', [])
    for product_id in product_ids:
        product = Product.query.get(product_id)
        if product:
            template.products.append(product)
    db.session.commit()

    log = SysOperLog(title='提示词模板', business_type=1, oper_name=g.username, oper_url='/api/prompt-templates', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@prompt_bp.route('/<int:template_id>', methods=['PUT'])
@token_required
def update_prompt_template(template_id):
    template = PromptTemplate.query.get(template_id)
    if not template:
        return jsonify({'code': 404, 'msg': '模板不存在', 'data': None})

    data = request.get_json()
    if 'name' in data:
        template.name = data['name']
    if 'promptContent' in data:
        template.prompt_content = data['promptContent']
    if 'requiredParagraphs' in data:
        template.required_paragraphs = data['requiredParagraphs']
    if 'businessType' in data:
        template.business_type = data['businessType']
    if 'status' in data:
        template.status = data['status']

    if 'productIds' in data:
        template.products.clear()
        product_ids = data['productIds']
        for product_id in product_ids:
            product = Product.query.get(product_id)
            if product:
                template.products.append(product)

    db.session.commit()

    log = SysOperLog(title='提示词模板', business_type=2, oper_name=g.username, oper_url=f'/api/prompt-templates/{template_id}', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@prompt_bp.route('/<int:template_id>', methods=['DELETE'])
@token_required
def delete_prompt_template(template_id):
    template = PromptTemplate.query.get(template_id)
    if not template:
        return jsonify({'code': 404, 'msg': '模板不存在', 'data': None})

    db.session.delete(template)
    db.session.commit()

    log = SysOperLog(title='提示词模板', business_type=3, oper_name=g.username, oper_url=f'/api/prompt-templates/{template_id}', status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@prompt_bp.route('/<int:template_id>/default', methods=['PUT'])
@token_required
def set_prompt_default(template_id):
    template = PromptTemplate.query.get(template_id)
    if not template:
        return jsonify({'code': 404, 'msg': '模板不存在', 'data': None})

    PromptTemplate.query.update({'is_default': 0})
    template.is_default = 1
    db.session.commit()

    return jsonify({'code': 200, 'msg': '设置成功', 'data': None})


@prompt_bp.route('/all', methods=['GET'])
@token_required
def get_all_prompt_templates():
    templates = PromptTemplate.query.filter_by(status=0).all()
    template_list = []
    for t in templates:
        product_ids = [p.id for p in t.products]
        product_names = [p.name for p in t.products]
        template_list.append({
            'id': t.id,
            'name': t.name,
            'productIds': product_ids,
            'productNames': product_names
        })
    return jsonify({'code': 200, 'msg': 'success', 'data': template_list})
