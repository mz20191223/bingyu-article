from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, PublishRecord
from app.services.publish_service import generate_article, publish_article

bp = Blueprint('publish', __name__)


@bp.route('/generate', methods=['POST'])
@token_required
def generate():
    data = request.get_json()
    product_id = data.get('productId')
    website_ids = data.get('websiteIds', [])
    content_template_id = data.get('contentTemplateId')
    title_template_id = data.get('titleTemplateId')
    model_id = data.get('modelId')
    keyword_ids = data.get('keywordIds', [])

    if not product_id:
        return jsonify({'code': 400, 'msg': '请选择产品', 'data': None})
    if not website_ids:
        return jsonify({'code': 400, 'msg': '请选择目标网站', 'data': None})

    try:
        result = generate_article(product_id, website_ids, content_template_id, title_template_id, model_id, keyword_ids)
        return jsonify({'code': 200, 'msg': '生成成功', 'data': result})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'生成失败: {str(e)}', 'data': None})


@bp.route('/submit', methods=['POST'])
@token_required
def submit():
    data = request.get_json()
    product_id = data.get('productId')
    website_ids = data.get('websiteIds', [])
    title = data.get('title')
    content = data.get('content')
    model_id = data.get('modelId')
    title_template_id = data.get('titleTemplateId')
    content_template_id = data.get('contentTemplateId')

    if not product_id:
        return jsonify({'code': 400, 'msg': '请选择产品', 'data': None})
    if not website_ids:
        return jsonify({'code': 400, 'msg': '请选择目标网站', 'data': None})
    if not title or not content:
        return jsonify({'code': 400, 'msg': '标题和内容不能为空', 'data': None})

    try:
        result = publish_article(product_id, website_ids, title, content, model_id, title_template_id, content_template_id, g.user_id)
        return jsonify({'code': 200, 'msg': '发布成功', 'data': result})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'发布失败: {str(e)}', 'data': None})
