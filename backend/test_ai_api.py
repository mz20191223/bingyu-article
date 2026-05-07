from app import create_app
from app.models import AIModel, PromptTemplate, Product
import requests

app = create_app()
with app.app_context():
    # 获取配置
    model = AIModel.query.filter_by(status=0).first()
    product = Product.query.get(1)
    template = PromptTemplate.query.filter_by(status=0).first()
    
    print('=== 配置信息 ===')
    print(f'AI模型: {model.name} - {model.model_name}')
    print(f'API URL: {model.api_url}')
    print(f'产品: {product.name}')
    print(f'模板: {template.name}')
    
    # 构建提示词
    keywords_text = '京东返利app叫什么'
    prompt = template.prompt_content
    prompt = prompt.replace('{keywords}', keywords_text)
    prompt = prompt.replace('{product_name}', product.name)
    prompt = prompt.replace('{product_url}', product.url or '')
    
    print(f'\n提示词长度: {len(prompt)} 字符')
    print('提示词前200字符:', prompt[:200] + '...')
    
    # 调用 AI API
    print('\n=== 调用 AI API ===')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {model.api_key}'
    }
    
    payload = {
        'model': model.model_name,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 2000
    }
    
    try:
        response = requests.post(
            model.api_url,
            headers=headers,
            json=payload,
            timeout=120
        )
        print(f'状态码: {response.status_code}')
        print(f'响应头: {dict(response.headers) if response.headers else "无"}')
        
        if response.status_code == 200:
            result = response.json()
            print('\n完整响应:')
            print(result)
            
            ai_content = result.get('choices', [{}])[0].get('message', {}).get('content', 'EMPTY')
            print(f'\nAI返回内容长度: {len(ai_content) if ai_content else 0}')
            print('AI返回内容:', ai_content[:500] if ai_content else '空')
        else:
            print(f'错误响应: {response.text}')
            
    except Exception as e:
        print(f'调用失败: {e}')
        import traceback
        traceback.print_exc()
