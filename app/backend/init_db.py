from init import create_app, db
from models import Book

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized successfully.")
