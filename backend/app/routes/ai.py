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
    print(f"DEBUG: 请求数据: {data}")

    keywords_str = data.get('keywords', '')
    template_id = data.get('templateId')
    product_id = data.get('productId')
    print(f"DEBUG: keywords_str={keywords_str}, template_id={template_id}, product_id={product_id}")

    keywords_list = [k.strip() for k in keywords_str.split(',') if k.strip()] if keywords_str else []
    keywords_text = '、'.join(keywords_list) if keywords_list else ''
    print(f"DEBUG: keywords_list={keywords_list}, keywords_text={keywords_text}")

    product_name = ''
    product_url = ''
    if product_id:
        product = Product.query.get(product_id)
        if product:
            product_name = product.name
            product_url = product.url or ''

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
        print(f"DEBUG: 所有可用模板: {[t.name for t in templates]}")
        if templates:
            template = templates[0]

    if not template:
        print("DEBUG: 未找到可用模板")
        return jsonify({'code': 404, 'msg': '未找到可用的提示词模板', 'data': None})
    
    print(f"DEBUG: 使用模板: {template.name}, ID: {template.id}")

    prompt = template.prompt_content
    # 替换占位符，同时支持 {keywords} 和 {keyword}
    prompt = prompt.replace('{keywords}', keywords_text)
    prompt = prompt.replace('{keyword}', keywords_text)
    prompt = prompt.replace('{product_name}', product_name)
    prompt = prompt.replace('{product_url}', product_url)
    print(f"DEBUG: 提示词长度: {len(prompt)}")
    print(f"DEBUG: 替换后的关键词: {keywords_text}")

    try:
        model = AIModel.query.filter_by(status=0).first()
        print(f"DEBUG: AI模型: {model.name if model else None}, API Key存在: {bool(model and model.api_key)}")
        
        if not model or not model.api_key:
            print("DEBUG: 无AI模型或API Key，使用模板内容")
            title, body = parse_ai_content(prompt)
            
            if template.conclusion_text and body:
                body = body + '\n\n' + template.conclusion_text
            
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

        # 在prompt前添加前置指令，强制模型直接输出结果，不输出任何思考过程
        direct_prompt = "【重要指令】你是专业文案生成器，严格遵守以下规则：1. 只输出最终结果，不输出任何分析、解释、思考过程或格式说明！2. 直接开始写标题和正文，不要写'首先'、'我来分析'等开头语！3. 严格按照用户后续要求的格式输出，不要增加任何额外内容！\n\n" + prompt
        
        payload = {
            'model': model.model_name,
            'messages': [{'role': 'user', 'content': direct_prompt}],
            'max_tokens': 3000,
            'temperature': 0.7,
            'top_p': 0.9,
            'stream': False,
            'thinking': {'type': 'disabled'},  # 正确禁用思维链的参数
            'response_format': {'type': 'text'}
        }
        print(f"DEBUG: 请求payload: {json.dumps(payload, ensure_ascii=False)}")

        print(f"DEBUG: 准备调用AI API: {model.api_url}")
        response = requests.post(
            model.api_url,
            headers=headers,
            json=payload,
            timeout=120
        )
        print(f"DEBUG: API响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"DEBUG: API响应长度: {len(str(result))}")
            print(f"DEBUG: API响应结构keys: {list(result.keys())}")
            
            # 检查choices字段
            choices = result.get('choices', [])
            print(f"DEBUG: choices长度: {len(choices)}")
            
            if choices:
                first_choice = choices[0]
                print(f"DEBUG: first_choice结构keys: {list(first_choice.keys())}")
                
                message = first_choice.get('message', {})
                print(f"DEBUG: message结构keys: {list(message.keys())}")
                
                ai_content = message.get('content', '')
                reasoning_content = message.get('reasoning_content', '')
                
                print(f"DEBUG: content字段长度: {len(ai_content) if ai_content else 0}")
                print(f"DEBUG: reasoning_content字段长度: {len(reasoning_content) if reasoning_content else 0}")
                
                # 优先使用content字段
                if ai_content and ai_content.strip() and len(ai_content.strip()) >= 100:
                    # content有效，直接使用
                    pass
                elif reasoning_content and reasoning_content.strip():
                    # content无效，但reasoning_content有内容
                    reasoning = reasoning_content.strip()
                    
                    # 策略：从reasoning_content中提取真正的文章内容
                    # 真正的文章结构：标题 + 【小标题】内容 + ... + 【结尾引导】
                    
                    # 1. 找到【结尾引导】的位置
                    end_guide_pos = reasoning.find('【结尾引导】')
                    
                    if end_guide_pos != -1:
                        content_before_guide = reasoning[:end_guide_pos]
                        
                        # 2. 找所有正文小标题【的位置（小标题通常8-30字）
                        bracket_positions = []
                        for i in range(len(content_before_guide)):
                            if content_before_guide[i] == '【':
                                end_bracket = content_before_guide.find('】', i+1)
                                if end_bracket != -1:
                                    title_length = end_bracket - i - 1
                                    if title_length >= 8 and title_length <= 30:
                                        bracket_positions.append(i)
                        
                        # 3. 如果找到了多个小标题，正文应该在最后几个小标题附近
                        if bracket_positions:
                            # 取倒数第2或第3个小标题的位置，缩小搜索范围
                            target_idx = max(0, len(bracket_positions) - 3)
                            target_bracket_pos = bracket_positions[target_idx]
                            
                            # 只在目标小标题前300字符范围内搜索标题
                            search_start = max(0, target_bracket_pos - 300)
                            search_end = target_bracket_pos
                            
                            # 在这个范围内找标题
                            search_area = content_before_guide[search_start:search_end]
                            lines = search_area.split('\n')
                            title_line = ''
                            
                            for line in reversed(lines):
                                line = line.strip()
                                if line:
                                    # 排除格式说明和思考过程的行
                                    if '格式要求' in line or '内容要求' in line or '标题：' in line or '标题:' in line or line.startswith('1.') or line.startswith('2.') or line.startswith('3.') or '要求如下' in line or '任务是' in line or '用户要求' in line or '用户说' in line or '我需要' in line or '首先' in line or '让我' in line or '**' in line or '---' in line:
                                        continue
                                    # 标题通常15-35字，不包含冒号、星号等特殊格式
                                    if len(line) >= 15 and len(line) <= 40 and ':' not in line and '*' not in line:
                                        title_line = line
                                        break
                            
                            if title_line:
                                # 从标题开始提取
                                title_start_pos = content_before_guide.rfind(title_line, search_start, search_end)
                                if title_start_pos != -1:
                                    ai_content = reasoning[title_start_pos:end_guide_pos]
                                else:
                                    # 找不到标题位置，从目标小标题开始
                                    ai_content = reasoning[target_bracket_pos:end_guide_pos]
                            else:
                                # 找不到标题，从目标小标题开始
                                ai_content = reasoning[target_bracket_pos:end_guide_pos]
                        else:
                            ai_content = content_before_guide
                    else:
                        ai_content = reasoning
                else:
                    ai_content = ''
            else:
                ai_content = prompt
                
            print(f"DEBUG: AI返回内容长度: {len(ai_content) if ai_content else 0}")
            print(f"DEBUG: AI返回内容前100字符: {ai_content[:100] if ai_content else '空'}")

            title, body = parse_ai_content(ai_content)
            print(f"DEBUG: 解析结果 - title={title}, body长度={len(body) if body else 0}")
            
            if template.conclusion_text and body:
                body = body + '\n\n' + template.conclusion_text

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
            print(f"DEBUG: AI API调用失败，状态码: {response.status_code}")
            return jsonify({'code': 500, 'msg': 'AI生成失败', 'data': None})

    except Exception as e:
        print(f"DEBUG: 异常: {e}")
        import traceback
        traceback.print_exc()
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
