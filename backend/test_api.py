import requests
import json

# 测试合成API
url = "http://localhost:5000/api/images/8/composite"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiYWRtaW4iOmZhbHNlLCJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE3NzgwNjg4MDB9.Xn5kE9l65q6X5kE9l65q6X5kE9l65q6X5kE9l65q6"
}

data = {
    "text_overlay": json.dumps({
        "text": "088886",
        "fontSize": "large",
        "color": "red",
        "bgStyle": "none",
        "positionX": 45.19,
        "positionY": 28.67,
        "bold": True
    })
}

try:
    response = requests.put(url, headers=headers, json=data)
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"合成成功！图片URL: {result.get('data', {}).get('compositeUrl')}")
    else:
        print("合成失败")
except Exception as e:
    print(f"请求失败: {e}")
