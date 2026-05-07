import sys
sys.path.insert(0, 'backend')

from app import create_app, db
from app.models import Website

app = create_app()
with app.app_context():
    websites = Website.query.all()
    for w in websites:
        print(f"\n=== 网站: {w.name} (ID: {w.id}) ===")
        print(f"  code: {w.code}")
        print(f"  login_url: {w.login_url}")
        print(f"  publish_url: {w.publish_url}")
        print(f"  username: {w.username}")
        print(f"  password: {w.password}")
        print(f"  username_selector: {w.username_selector}")
        print(f"  password_selector: {w.password_selector}")
        print(f"  login_button_selector: {w.login_button_selector}")
        print(f"  title_selector: {w.title_selector}")
        print(f"  content_selector: {w.content_selector}")
        print(f"  category_selector: {w.category_selector}")
        print(f"  publish_button_selector: {w.publish_button_selector}")
        print(f"  status: {w.status}")
        print(f"  is_default: {w.is_default}")