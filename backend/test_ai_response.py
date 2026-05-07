from app import create_app
from app.models import AIModel, PromptTemplate, Product
import requests

app = create_app()
with app.app_context():
    # 获取配置
    model = AIModel.query.filter_by(status=0).first()
    product = Product.query.get(1)
    template = PromptTemplate.query.filter_by(status=0).first()
    
    # 构建提示词
    keywords_text = '打车软件排行榜前十名'
    prompt = template.prompt_content
    prompt = prompt.replace('{keywords}', keywords_text)
    prompt = prompt.replace('{product_name}', product.name)
    prompt = prompt.replace('{product_url}', product.url or '')
    
    print('=== 调用 AI API ===')
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
        model.api_url,
        headers=headers,
        json=payload,
        timeout=120
    )
    
    print(f'状态码: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        print('\n=== 完整响应结构 ===')
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        print('\n=== 响应结构分析 ===')
        print(f"响应keys: {list(result.keys())}")
        
        choices = result.get('choices', [])
        print(f"choices长度: {len(choices)}")
        
        if choices:
            first_choice = choices[0]
            print(f"first_choice keys: {list(first_choice.keys())}")
            
            message = first_choice.get('message', {})
            print(f"message keys: {list(message.keys())}")
            
            # 检查所有可能的字段
            for key in message:
                value = message[key]
                if isinstance(value, str):
                    print(f"  {key}: 长度={len(value)}, 前50字符='{value[:50]}...'")
                else:
                    print(f"  {key}: {type(value)}")
