import requests
import json

BASE_URL = "http://localhost:5000/api"

def login():
    login_data = {
        "username": "admin",
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        result = response.json()
        return result.get('data', {}).get('token')
    return None

def test_prompt_templates():
    token = login()
    if not token:
        print("登录失败")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n=== 测试提示词模板管理 ===")
    
    print("\n1. 获取模板列表")
    response = requests.get(f"{BASE_URL}/prompt-templates", headers=headers)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"结果: {json.dumps(result, ensure_ascii=False)}")
    
    print("\n2. 获取模板选项")
    response = requests.get(f"{BASE_URL}/prompt-templates/options", headers=headers)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"结果: {json.dumps(result, ensure_ascii=False)}")
    
    print("\n3. 获取默认模板")
    response = requests.get(f"{BASE_URL}/prompt-templates/default", headers=headers)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"结果: {json.dumps(result, ensure_ascii=False)}")
    
    print("\n4. 创建新模板")
    new_template = {
        "name": "测试模板",
        "business_type": "推广软文",
        "required_paragraphs": 5,
        "prompt_content": "请写一篇关于{product_name}的推广文章，关键词：{keywords}。\n\n要求：\n- 标题吸引人\n- 至少5个段落\n- 每个段落用【小标题】开头\n- 段落间空一行\n- 纯文本格式",
        "conclusion_text": "【结语】\n\n感谢阅读！如果你觉得这篇文章对你有帮助，请分享给更多朋友。",
        "is_default": 0,
        "product_ids": []
    }
    response = requests.post(f"{BASE_URL}/prompt-templates", headers=headers, json=new_template)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"结果: {json.dumps(result, ensure_ascii=False)}")
    
    if result.get('code') == 200:
        template_id = result.get('data', {}).get('id')
        
        print(f"\n5. 获取单个模板 (ID: {template_id})")
        response = requests.get(f"{BASE_URL}/prompt-templates/{template_id}", headers=headers)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"结果: {json.dumps(result, ensure_ascii=False)}")
        
        print(f"\n6. 更新模板")
        update_data = {
            "name": "测试模板(更新)",
            "business_type": "推广软文",
            "required_paragraphs": 6,
            "prompt_content": "更新后的提示词内容",
            "conclusion_text": "更新后的结尾引导",
            "is_default": 0,
            "product_ids": []
        }
        response = requests.put(f"{BASE_URL}/prompt-templates/{template_id}", headers=headers, json=update_data)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"结果: {json.dumps(result, ensure_ascii=False)}")

if __name__ == "__main__":
    test_prompt_templates()