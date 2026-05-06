from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, ContentPromptTemplate, TitlePromptTemplate, SysOperLog, Product, content_template_product, title_template_product

content_bp = Blueprint('content_templates', __name__)
title_bp = Blueprint('title_templates', __name__)


@content_bp.route('', methods=['GET'])
@token_required
def get_content_templates():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    product_id = request.args.get('productId', type=int)
    status = request.args.get('status', type=int)

    query = ContentPromptTemplate.query

    if status is not None:
        query = query.filter(ContentPromptTemplate.status == status)

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
            'businessType': t.business_type,
            'metaTitle': t.meta_title,
            'metaDescription': t.meta_description,
            'keywordPrompt': t.keyword_prompt,
            'contentPrompt': t.content_prompt,
            'conclusionPrompt': t.conclusion_prompt,
            'isDefault': t.is_default,
            'status': t.status,
            'createTime': t.create_time.strftime('%Y-%m-%d %H:%M:%S') if t.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': template_list, 'total': total, 'page': page, 'pageSize': page_size}})


@content_bp.route('', methods=['POST'])
@token_required
def create_content_template():
    data = request.get_json()
    name = data.get('name')
    content_prompt = data.get('contentPrompt')

    if not name or not content_prompt:
        return jsonify({'code': 400, 'msg': '模板名称和内容提示词不能为空', 'data': None})

    template = ContentPromptTemplate(
        name=name,
        business_type=data.get('businessType'),
        meta_title=data.get('metaTitle'),
        meta_description=data.get('metaDescription'),
        keyword_prompt=data.get('keywordPrompt'),
        content_prompt=content_prompt,
        conclusion_prompt=data.get('conclusionPrompt'),
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

    log = SysOperLog(title='内容模板', business_type=1, oper_name=g.username, oper_url='/api/content-templates', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@content_bp.route('/<int:template_id>', methods=['PUT'])
@token_required
def update_content_template(template_id):
    template = ContentPromptTemplate.query.get(template_id)
    if not template:
        return jsonify({'code': 404, 'msg': '模板不存在', 'data': None})

    data = request.get_json()
    if 'name' in data:
        template.name = data['name']
    if 'businessType' in data:
        template.business_type = data['businessType']
    if 'metaTitle' in data:
        template.meta_title = data['metaTitle']
    if 'metaDescription' in data:
        template.meta_description = data['metaDescription']
    if 'keywordPrompt' in data:
        template.keyword_prompt = data['keywordPrompt']
    if 'contentPrompt' in data:
        template.content_prompt = data['contentPrompt']
    if 'conclusionPrompt' in data:
        template.conclusion_prompt = data['conclusionPrompt']
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

    log = SysOperLog(title='内容模板', business_type=2, oper_name=g.username, oper_url=f'/api/content-templates/{template_id}', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@content_bp.route('/<int:template_id>', methods=['DELETE'])
@token_required
def delete_content_template(template_id):
    template = ContentPromptTemplate.query.get(template_id)
    if not template:
        return jsonify({'code': 404, 'msg': '模板不存在', 'data': None})

    db.session.delete(template)
    db.session.commit()

    log = SysOperLog(title='内容模板', business_type=3, oper_name=g.username, oper_url=f'/api/content-templates/{template_id}', status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@content_bp.route('/<int:template_id>/default', methods=['PUT'])
@token_required
def set_content_default(template_id):
    template = ContentPromptTemplate.query.get(template_id)
    if not template:
        return jsonify({'code': 404, 'msg': '模板不存在', 'data': None})

    ContentPromptTemplate.query.update({'is_default': 0})
    template.is_default = 1
    db.session.commit()

    return jsonify({'code': 200, 'msg': '设置成功', 'data': None})


@title_bp.route('', methods=['GET'])
@token_required
def get_title_templates():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    product_id = request.args.get('productId', type=int)
    status = request.args.get('status', type=int)

    query = TitlePromptTemplate.query

    if status is not None:
        query = query.filter(TitlePromptTemplate.status == status)

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
            'businessType': t.business_type,
            'titlePrompt': t.title_prompt,
            'isDefault': t.is_default,
            'status': t.status,
            'createTime': t.create_time.strftime('%Y-%m-%d %H:%M:%S') if t.create_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': template_list, 'total': total, 'page': page, 'pageSize': page_size}})


@title_bp.route('', methods=['POST'])
@token_required
def create_title_template():
    data = request.get_json()
    name = data.get('name')
    title_prompt = data.get('titlePrompt')

    if not name or not title_prompt:
        return jsonify({'code': 400, 'msg': '模板名称和标题提示词不能为空', 'data': None})

    template = TitlePromptTemplate(
        name=name,
        business_type=data.get('businessType'),
        title_prompt=title_prompt,
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

    log = SysOperLog(title='标题模板', business_type=1, oper_name=g.username, oper_url='/api/title-templates', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '创建成功', 'data': None})


@title_bp.route('/<int:template_id>', methods=['PUT'])
@token_required
def update_title_template(template_id):
    template = TitlePromptTemplate.query.get(template_id)
    if not template:
        return jsonify({'code': 404, 'msg': '模板不存在', 'data': None})

    data = request.get_json()
    if 'name' in data:
        template.name = data['name']
    if 'businessType' in data:
        template.business_type = data['businessType']
    if 'titlePrompt' in data:
        template.title_prompt = data['titlePrompt']
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

    log = SysOperLog(title='标题模板', business_type=2, oper_name=g.username, oper_url=f'/api/title-templates/{template_id}', oper_param=str(data), status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '更新成功', 'data': None})


@title_bp.route('/<int:template_id>', methods=['DELETE'])
@token_required
def delete_title_template(template_id):
    template = TitlePromptTemplate.query.get(template_id)
    if not template:
        return jsonify({'code': 404, 'msg': '模板不存在', 'data': None})

    db.session.delete(template)
    db.session.commit()

    log = SysOperLog(title='标题模板', business_type=3, oper_name=g.username, oper_url=f'/api/title-templates/{template_id}', status=0)
    db.session.add(log)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '删除成功', 'data': None})


@title_bp.route('/<int:template_id>/default', methods=['PUT'])
@token_required
def set_title_default(template_id):
    template = TitlePromptTemplate.query.get(template_id)
    if not template:
        return jsonify({'code': 404, 'msg': '模板不存在', 'data': None})

    TitlePromptTemplate.query.update({'is_default': 0})
    template.is_default = 1
    db.session.commit()

    return jsonify({'code': 200, 'msg': '设置成功', 'data': None})
