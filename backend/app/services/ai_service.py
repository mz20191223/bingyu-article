import requests
from app.models import AIModel, ContentPromptTemplate, TitlePromptTemplate, Product, Keyword

class AIService:
    def __init__(self, model_id=None):
        if model_id:
            self.model = AIModel.query.get(model_id)
        else:
            self.model = AIModel.query.filter_by(status=0).first()
        if not self.model:
            raise Exception('AI模型不存在')

    def generate_title(self, product_id, title_template_id=None, keywords=None):
        product = Product.query.get(product_id) if product_id else None

        if title_template_id:
            template = TitlePromptTemplate.query.get(title_template_id)
        elif product_id:
            # 查询与该产品关联的模板
            template = TitlePromptTemplate.query.filter(
                TitlePromptTemplate.status == 0,
                TitlePromptTemplate.products.any(id=product_id)
            ).first()
            if not template:
                # 如果没有关联产品的模板，查找默认模板
                template = TitlePromptTemplate.query.filter_by(is_default=1, status=0).first()
        else:
            template = TitlePromptTemplate.query.filter_by(is_default=1, status=0).first()

        if not template:
            templates = TitlePromptTemplate.query.filter_by(status=0).all()
            if templates:
                template = templates[0]

        if not template:
            return f'{product.name if product else "产品"} - 最佳选择'

        prompt = template.title_prompt or '{product_name}'
        keyword_str = ', '.join([k.keyword for k in keywords]) if keywords else ''

        prompt = prompt.replace('{product_name}', product.name if product else '')
        prompt = prompt.replace('{keywords}', keyword_str)
        prompt = prompt.replace('{description}', product.description if product and product.description else '')

        return self._call_api(prompt, max_tokens=50)

    def generate_content(self, product_id, content_template_id=None, keywords=None):
        product = Product.query.get(product_id) if product_id else None

        if content_template_id:
            template = ContentPromptTemplate.query.get(content_template_id)
        elif product_id:
            # 查询与该产品关联的模板
            template = ContentPromptTemplate.query.filter(
                ContentPromptTemplate.status == 0,
                ContentPromptTemplate.products.any(id=product_id)
            ).first()
            if not template:
                # 如果没有关联产品的模板，查找默认模板
                template = ContentPromptTemplate.query.filter_by(is_default=1, status=0).first()
        else:
            template = ContentPromptTemplate.query.filter_by(is_default=1, status=0).first()

        if not template:
            templates = ContentPromptTemplate.query.filter_by(status=0).all()
            if templates:
                template = templates[0]

        if not template:
            return f'{product.description if product and product.description else product.name if product else "产品描述"}'

        prompt = template.content_prompt or '{product_name}: {description}'
        keyword_str = ', '.join([k.keyword for k in keywords]) if keywords else ''

        prompt = prompt.replace('{product_name}', product.name if product else '')
        prompt = prompt.replace('{keywords}', keyword_str)
        prompt = prompt.replace('{description}', product.description if product and product.description else '')

        return self._call_api(prompt, max_tokens=500)

    def _call_api(self, prompt, max_tokens=200):
        if not self.model or not self.model.api_key:
            return prompt

        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.model.api_key}'
            }

            payload = {
                'model': self.model.model_name,
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': max_tokens
            }

            response = requests.post(
                f'{self.model.api_url}/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('choices', [{}])[0].get('message', {}).get('content', prompt)
            else:
                return prompt
        except Exception as e:
            print(f'AI API调用失败: {e}')
            return prompt
