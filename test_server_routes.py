import requests

BASE_URL = "http://localhost:5000"

# 获取所有路由
response = requests.get(f"{BASE_URL}/")
print(f"根路径: {response.status_code}")

# 尝试获取一些已知存在的路由
known_routes = ['/api/products', '/api/websites', '/api/records']
for r in known_routes:
    response = requests.get(r)
    print(f"GET {r}: {response.status_code}")

# 测试drafts
response = requests.get(f"{BASE_URL}/api/drafts")
print(f"\nGET /api/drafts: {response.status_code}")
print(f"Response: {response.text[:200]}")