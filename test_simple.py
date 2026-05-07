import requests

BASE_URL = "http://localhost:5000"

response = requests.get(f"{BASE_URL}/api/drafts")
print(f"GET /api/drafts: {response.status_code}")
print(f"Response: {response.text[:300]}")