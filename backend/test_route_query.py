from app import create_app
from app.models import PromptTemplate, Product, AIModel

app = create_app()
with app.app_context():
    product_id = 1
    
    print('=== 测试路由中的查询逻辑 ===')
    print(f'product_id: {product_id}')
    
    # 模拟路由中的查询逻辑
    template = None
    
    # 进入 elif product_id: 分支
    print('\n1. 查询产品关联的模板:')
    template = PromptTemplate.query.filter(
        PromptTemplate.status == 0,
        PromptTemplate.products.any(id=product_id)
    ).first()
    print(f'   查询结果: {template.name if template else None}')
    
    if not template:
        print('\n2. 查询默认模板:')
        template = PromptTemplate.query.filter_by(is_default=1, status=0).first()
        print(f'   查询结果: {template.name if template else None}')
    
    if not template:
        print('\n3. 查询所有可用模板:')
        templates = PromptTemplate.query.filter_by(status=0).all()
        if templates:
            template = templates[0]
        print(f'   查询结果: {template.name if template else None}')
    
    print(f'\n最终模板: {template.name if template else None}')
    
    # 检查模板内容
    if template:
        print(f'\n模板内容长度: {len(template.prompt_content)}')
        print(f'模板内容前100字符: {template.prompt_content[:100]}...')
        
        # 检查关键词替换
        keywords_text = '京东返利app叫什么'
        product = Product.query.get(product_id)
        prompt = template.prompt_content
        prompt = prompt.replace('{keywords}', keywords_text)
        prompt = prompt.replace('{product_name}', product.name if product else '')
        prompt = prompt.replace('{product_url}', product.url or '')
        
        print(f'\n替换后的提示词长度: {len(prompt)}')
        
    # 检查AI模型
    print('\n=== AI模型检查 ===')
    model = AIModel.query.filter_by(status=0).first()
    print(f'AI模型: {model.name if model else None}')
    print(f'API Key: {"存在" if model and model.api_key else "不存在"}')
