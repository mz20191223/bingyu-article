from app import create_app
from app.models import AIModel, PromptTemplate

app = create_app()
with app.app_context():
    print('=== AI模型 ===')
    models = AIModel.query.all()
    for m in models:
        print(f'{m.id}: {m.name} - {m.model_name}')
        print(f'  API URL: {m.api_url[:50] if m.api_url else "None"}')
        print(f'  API Key: {m.api_key[:20] if m.api_key else "None"}...')
        print(f'  状态: {m.status}')
    
    print('\n=== 提示词模板 ===')
    templates = PromptTemplate.query.all()
    for t in templates:
        print(f'{t.id}: {t.name} - 默认:{t.is_default} - 状态:{t.status}')
        print(f'  模板内容预览: {t.prompt_content[:100] if t.prompt_content else "None"}...')
