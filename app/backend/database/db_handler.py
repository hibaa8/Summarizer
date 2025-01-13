from . import db
from .models import Book
from flask import jsonify

class DatabaseHandler:
    def add_book(self, book):   
        try:
            existing_book = Book.query.filter_by(title=book["title"]).first()
            if existing_book:
                print(f"Book already exists in the database: {book['title']}")
                return
            book_record = Book(
                title=book["title"],
                author=book["author"],
                language=book["language"],
                subject=book["subject"],
                image_url=book["image_url"],
                amazon_url=book["amazon_url"],
                summary=book["summary"],
            )
            db.session.add(book_record)
            db.session.commit()

        except Exception as e:
            db.session.rollback() 
            print(f"Error while adding books to database: {e}")

    def get_all_books(self,subject):
        try:
            query = Book.query
            if subject:
                query = query.filter(Book.subject.contains(subject))
            books = query.all()
            print(f"Query results: {books}")
            books_data = [
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "language": book.language,
                    "subject": book.subject,
                    "image_url": book.image_url,
                    "amazon_url": book.amazon_url,
                    "summary": book.summary,
                }
                for book in books
            ]
            return jsonify(books_data)

        except Exception as e:
            print(f"Error while retrieving books: {e}")
            return []

    def get_book_by_id(self, book_id):
        try:
            book = Book.query.get_or_404(book_id) 
            return jsonify({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "language": book.language,
            "subject": book.subject,
            "image_url": book.image_url,
            "amazon_url": book.amazon_url,
            "summary": book.summary
        })
        except Exception as e:
            print(f"Error while retrieving book by title: {e}")
            return None
