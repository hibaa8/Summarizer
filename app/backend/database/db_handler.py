from . import db
from .models import Book
from flask import jsonify

class DatabaseHandler:
    def add_book(self, book):
        """
        Adds one book to the database.

        :param books_metadata: List of book metadata dictionaries.
        """
        
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
        """
        Retrieve all books from the database.

        :return: List of Book objects.
        """
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
        """
        Retrieve a single book by its id.

        :param title: Title of the book to retrieve.
        :return: Book object or None if not found.
        """
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
