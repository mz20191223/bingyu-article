from app import create_app
from app.models import db, Image

app = create_app()
with app.app_context():
    images = Image.query.all()
    for img in images:
        print(f"ID: {img.id}, URL: {img.url}, Composite URL: {img.composite_url}")
