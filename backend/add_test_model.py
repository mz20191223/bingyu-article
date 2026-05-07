"""
添加测试AI模型
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, AIModel

app = create_app()

with app.app_context():
    # 检查是否已有模型
    existing_model = AIModel.query.first()
    if existing_model:
        print(f"已存在模型: ID={existing_model.id}, 名称={existing_model.model_name}, 状态={existing_model.status}")
        
        # 如果状态为禁用，启用它
        if existing_model.status == 1:
            existing_model.status = 0
            db.session.commit()
            print("已启用现有模型")
    else:
        # 创建测试模型
        test_model = AIModel(
            name='测试模型',
            provider='openai',
            model_name='gpt-3.5-turbo',
            api_key='test-key-for-development',
            api_url='https://api.openai.com/v1',
            status=0,
            is_default=1
        )
        db.session.add(test_model)
        db.session.commit()
        print(f"已创建测试模型: ID={test_model.id}")
    
    print("\n操作完成！")
