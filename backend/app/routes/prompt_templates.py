from flask import Blueprint, request, jsonify
from app.routes.auth import token_required
from app.models import db, PromptTemplate, Product
from datetime import datetime

prompt_bp = Blueprint('prompt_templates', __name__)


@prompt_bp.route('', methods=['GET'])
@token_required
def get_prompt_templates():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    product_id = request.args.get('product_id', type=int)
    name = request.args.get('name', '')
    
    query = PromptTemplate.query.filter_by(status=0).order_by(PromptTemplate.id.desc())
    
    if name:
        query = query.filter(PromptTemplate.name.like(f'%{name}%'))
    
    if product_id:
        query = query.join(PromptTemplate.products).filter(Product.id == product_id)
    
    pagination = query.paginate(page=page, per_page=size, error_out=False)
    
    result = []
    for template in pagination.items:
        product_ids = [p.id for p in template.products]
        product_names = [p.name for p in template.products]
        result.append({
            'id': template.id,
            'name': template.name,
            'prompt_content': template.prompt_content,
            'required_paragraphs': template.required_paragraphs,
            'business_type': template.business_type,
            'conclusion_text': template.conclusion_text,
            'is_default': template.is_default,
            'status': template.status,
            'product_ids': product_ids,
            'product_names': product_names,
            'create_time': template.create_time.strftime('%Y-%m-%d %H:%M:%S') if template.create_time else None,
            'update_time': template.update_time.strftime('%Y-%m-%d %H:%M:%S') if template.update_time else None
        })
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'list': result,
            'page': page,
            'pageSize': size,
            'total': pagination.total
        }
    })


@prompt_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_prompt_template(id):
    template = PromptTemplate.query.get_or_404(id)
    product_ids = [p.id for p in template.products]
    product_names = [p.name for p in template.products]
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'id': template.id,
            'name': template.name,
            'prompt_content': template.prompt_content,
            'required_paragraphs': template.required_paragraphs,
            'business_type': template.business_type,
            'conclusion_text': template.conclusion_text,
            'is_default': template.is_default,
            'status': template.status,
            'product_ids': product_ids,
            'product_names': product_names,
            'create_time': template.create_time.strftime('%Y-%m-%d %H:%M:%S') if template.create_time else None,
            'update_time': template.update_time.strftime('%Y-%m-%d %H:%M:%S') if template.update_time else None
        }
    })


@prompt_bp.route('', methods=['POST'])
@token_required
def create_prompt_template():
    data = request.get_json()
    
    name = data.get('name')
    prompt_content = data.get('prompt_content')
    
    if not name or not prompt_content:
        return jsonify({'code': 400, 'msg': '模板名称和提示词内容不能为空', 'data': None})
    
    template = PromptTemplate()
    template.name = name
    template.prompt_content = prompt_content
    template.required_paragraphs = data.get('required_paragraphs', 5)
    template.business_type = data.get('business_type')
    template.conclusion_text = data.get('conclusion_text')
    template.is_default = data.get('is_default', 0)
    
    if template.is_default == 1:
        PromptTemplate.query.update({'is_default': 0})
    
    db.session.add(template)
    db.session.flush()
    
    product_ids = data.get('product_ids', [])
    for product_id in product_ids:
        product = Product.query.get(product_id)
        if product:
            template.products.append(product)
    
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': '创建成功',
        'data': {
            'id': template.id
        }
    })


@prompt_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_prompt_template(id):
    template = PromptTemplate.query.get_or_404(id)
    data = request.get_json()
    
    template.name = data.get('name', template.name)
    template.prompt_content = data.get('prompt_content', template.prompt_content)
    template.required_paragraphs = data.get('required_paragraphs', template.required_paragraphs)
    template.business_type = data.get('business_type', template.business_type)
    template.conclusion_text = data.get('conclusion_text', template.conclusion_text)
    
    new_is_default = data.get('is_default', template.is_default)
    if new_is_default == 1 and template.is_default == 0:
        PromptTemplate.query.update({'is_default': 0})
    template.is_default = new_is_default
    
    product_ids = data.get('product_ids', [])
    template.products = []
    for product_id in product_ids:
        product = Product.query.get(product_id)
        if product:
            template.products.append(product)
    
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': '更新成功',
        'data': None
    })


@prompt_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_prompt_template(id):
    template = PromptTemplate.query.get_or_404(id)
    template.status = 1
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': '删除成功',
        'data': None
    })


@prompt_bp.route('/default/<int:id>', methods=['PUT'])
@token_required
def set_default_template(id):
    template = PromptTemplate.query.get_or_404(id)
    PromptTemplate.query.update({'is_default': 0})
    template.is_default = 1
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'msg': '设置默认成功',
        'data': None
    })


@prompt_bp.route('/default', methods=['GET'])
@token_required
def get_default_template():
    template = PromptTemplate.query.filter_by(is_default=1, status=0).first()
    
    if not template:
        template = PromptTemplate.query.filter_by(status=0).first()
    
    if template:
        product_ids = [p.id for p in template.products]
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': {
                'id': template.id,
                'name': template.name,
                'prompt_content': template.prompt_content,
                'required_paragraphs': template.required_paragraphs,
                'business_type': template.business_type,
                'conclusion_text': template.conclusion_text,
                'product_ids': product_ids
            }
        })
    else:
        return jsonify({
            'code': 200,
            'msg': 'success',
            'data': None
        })


@prompt_bp.route('/options', methods=['GET'])
@token_required
def get_template_options():
    templates = PromptTemplate.query.filter_by(status=0).order_by(PromptTemplate.id.desc()).all()
    
    options = []
    for template in templates:
        options.append({
            'value': template.id,
            'label': template.name
        })
    
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': options
    })