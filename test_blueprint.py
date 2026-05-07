import sys
sys.path.insert(0, 'backend')

from app import create_app

app = create_app()
with app.test_client() as client:
    response = client.get('/api/drafts')
    print(f"GET /api/drafts: {response.status_code}")
    print(f"Response: {response.data.decode()}")