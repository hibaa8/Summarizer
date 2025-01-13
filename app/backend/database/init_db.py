from backend.app import create_app
from database import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized successfully.")


# from init import create_app, db
# from models import Book

# app = create_app()

# with app.app_context():
#     db.create_all()
#     print("Database initialized successfully.")

# with app.app_context():
#     # Fetch the first two rows
#     last_two_books = Book.query.order_by(Book.id.desc()).limit(1).all()
    
#     if last_two_books:
#         for book in last_two_books:
#             db.session.delete(book)  # Delete each book
#         db.session.commit()  # Commit the changes
#         print("Successfully deleted the last two entries.")
#     else:
#         print("No entries found to delete.")