import os
import json
import uuid
from datetime import datetime
from app.models import db, AIModel, ContentPromptTemplate, TitlePromptTemplate, Image, Keyword, Product, Website, PublishRecord


class AIService:
    def __init__(self, model_id=None):
        if model_id:
            self.model = AIModel.query.get(model_id)
        else:
            self.model = AIModel.query.filter_by(is_default=1, status=0).first()
        if not self.model:
            raise Exception('未配置AI模型或模型已禁用')

    def generate_title(self, template_id, product, keywords):
        if template_id:
            template = TitlePromptTemplate.query.get(template_id)
        else:
            template = TitlePromptTemplate.query.filter_by(is_default=1, status=0).first()
        if not template:
            raise Exception('未配置标题模板')

        prompt = template.title_prompt
        prompt = prompt.replace('{product_name}', product.name if product else '')
        prompt = prompt.replace('{keywords}', ', '.join([k.keyword for k in keywords[:5]]) if keywords else '')

        return self._call_ai(prompt)

    def generate_content(self, template_id, product, keywords):
        if template_id:
            template = ContentPromptTemplate.query.get(template_id)
        else:
            template = ContentPromptTemplate.query.filter_by(is_default=1, status=0).first()
        if not template:
            raise Exception('未配置内容模板')

        prompt = template.content_prompt
        prompt = prompt.replace('{product_name}', product.name if product else '')
        prompt = prompt.replace('{product_url}', product.url if product else '')
        prompt = prompt.replace('{keywords}', ', '.join([k.keyword for k in keywords[:10]]) if keywords else '')

        conclusion = template.conclusion_prompt or ''
        conclusion = conclusion.replace('{product_name}', product.name if product else '')

        content = self._call_ai(prompt)
        if conclusion:
            content += '\n\n' + conclusion

        return content

    def _call_ai(self, prompt):
        if self.model.provider == 'openai':
            return self._call_openai(prompt)
        elif self.model.provider == 'zhipuai':
            return self._call_zhipuai(prompt)
        else:
            raise Exception(f'不支持的服务商: {self.model.provider}')

    def _call_openai(self, prompt):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.model.api_key, base_url=self.model.api_url)
            response = client.chat.completions.create(
                model=self.model.model_name or 'gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': prompt}],
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f'OpenAI调用失败: {str(e)}')

    def _call_zhipuai(self, prompt):
        try:
            import requests
            headers = {'Authorization': f'Bearer {self.model.api_key}'}
            data = {
                'prompt': prompt,
                'model': self.model.model_name or 'glm-4',
                'temperature': 0.8
            }
            response = requests.post(self.model.api_url, json=data, headers=headers, timeout=60)
            result = response.json()
            if result.get('code') == 200:
                return result['data']['choices'][0]['content']
            else:
                raise Exception(result.get('msg', '智谱AI调用失败'))
        except Exception as e:
            raise Exception(f'智谱AI调用失败: {str(e)}')


def generate_article(product_id, website_ids, content_template_id, title_template_id, model_id, keyword_ids):
    product = Product.query.get(product_id) if product_id else None
    if not product:
        raise Exception('产品不存在')

    keywords = []
    if keyword_ids:
        keywords = Keyword.query.filter(Keyword.id.in_(keyword_ids), Keyword.status == 0).all()
    else:
        keywords = Keyword.query.filter_by(status=0).limit(10).all()

    ai_service = AIService(model_id)

    title = ai_service.generate_title(title_template_id, product, keywords)
    content = ai_service.generate_content(content_template_id, product, keywords)

    images = Image.query.filter(
        Image.status == 0
    ).all()

    content_with_images = insert_images(content, images, website_ids)

    return {
        'title': title,
        'content': content_with_images['content'],
        'images': content_with_images['images']
    }


def insert_images(content, images, website_ids):
    if not images:
        return {'content': content, 'images': []}

    paragraphs = content.split('\n\n')
    result_images = []

    for img in images:
        result_images.append({'url': img.url, 'position_type': img.position_type, 'position_value': img.position_value})

    return {'content': content, 'images': result_images}


def publish_article(product_id, website_ids, title, content, model_id, title_template_id, content_template_id, user_id):
    task_id = str(uuid.uuid4())
    records = []
    websites = {}

    for website_id in website_ids:
        website = Website.query.get(website_id)
        if not website:
            continue
        websites[website_id] = website

        product = Product.query.get(product_id)
        record = PublishRecord(
            product_id=product_id,
            product_name=product.name if product else '',
            website_id=website_id,
            website_name=website.name,
            title=title,
            content=content,
            status='pending'
        )
        db.session.add(record)
        records.append(record)

    db.session.commit()

    for record in records:
        try:
            website = websites.get(record.website_id)
            if website:
                result = publish_to_website(record, website)
                record.status = 'success'
                record.result_url = result.get('url')
                record.publish_time = datetime.now()
            else:
                record.status = 'failed'
                record.error_msg = '网站不存在'
        except Exception as e:
            record.status = 'failed'
            record.error_msg = str(e)

    db.session.commit()

    return {'taskId': task_id, 'records': [{'id': r.id, 'websiteId': r.website_id, 'status': r.status} for r in records]}


def publish_to_website(record, website):
    import time
    time.sleep(1)

    return {'url': f'https://{website.code}.com/article/{record.id}'}