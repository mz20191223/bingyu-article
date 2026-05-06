from flask import Blueprint, request, jsonify
from app.models import PromptTemplate, Product, Keyword, AIModel
from app.services.ai_service import AIService
import requests

ai_bp = Blueprint('ai', __name__)


def parse_ai_content(content):
    if not content:
        return None, None

    lines = content.split('\n')
    if not lines:
        return None, None

    title = lines[0].strip() if lines[0].strip() else None
    body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else None

    return title, body


@ai_bp.route('/generate', methods=['POST'])
def generate_content():
    data = request.get_json()

    keyword = data.get('keyword')
    keywords_str = data.get('keywords', '')
    template_id = data.get('templateId')
    product_id = data.get('productId')

    if not keyword:
        return jsonify({'code': 400, 'msg': '关键词不能为空', 'data': None})

    keywords_list = [k.strip() for k in keywords_str.split(',') if k.strip()] if keywords_str else []
    keywords_text = '、'.join(keywords_list) if keywords_list else keyword

    template = None
    if template_id:
        template = PromptTemplate.query.get(template_id)
    elif product_id:
        template = PromptTemplate.query.filter(
            PromptTemplate.status == 0,
            PromptTemplate.products.any(id=product_id)
        ).first()
        if not template:
            template = PromptTemplate.query.filter_by(is_default=1, status=0).first()
    else:
        template = PromptTemplate.query.filter_by(is_default=1, status=0).first()

    if not template:
        templates = PromptTemplate.query.filter_by(status=0).all()
        if templates:
            template = templates[0]

    if not template:
        return jsonify({'code': 404, 'msg': '未找到可用的提示词模板', 'data': None})

    prompt = template.prompt_content
    prompt = prompt.replace('{keyword}', keyword)
    prompt = prompt.replace('{keywords}', keywords_text)

    try:
        model = AIModel.query.filter_by(status=0).first()
        if not model or not model.api_key:
            title, body = parse_ai_content(prompt)
            return jsonify({
                'code': 200,
                'msg': 'success',
                'data': {
                    'title': title,
                    'content': body,
                    'fullText': prompt
                }
            })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {model.api_key}'
        }

        payload = {
            'model': model.model_name,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 2000
        }

        response = requests.post(
            f'{model.api_url}/chat/completions',
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            ai_content = result.get('choices', [{}])[0].get('message', {}).get('content', prompt)

            title, body = parse_ai_content(ai_content)

            return jsonify({
                'code': 200,
                'msg': 'success',
                'data': {
                    'title': title,
                    'content': body,
                    'fullText': ai_content
                }
            })
        else:
            return jsonify({'code': 500, 'msg': 'AI生成失败', 'data': None})

    except Exception as e:
        return jsonify({'code': 500, 'msg': f'生成失败: {str(e)}', 'data': None})


@ai_bp.route('/keywords/random', methods=['GET'])
def get_random_keyword():
    count = request.args.get('count', 1, type=int)
    keywords = Keyword.query.filter_by(status=0).all()
    if not keywords:
        return jsonify({'code': 200, 'msg': 'success', 'data': []})

    import random
    selected = random.sample(keywords, min(count, len(keywords)))
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': [{'id': k.id, 'keyword': k.keyword} for k in selected]
    })
