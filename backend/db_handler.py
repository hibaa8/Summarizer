from init import create_app, db
from models import Book

class DatabaseHandler:
    def add_books(self, books):
        """
        Add a list of books to the database.

        :param books_metadata: List of book metadata dictionaries.
        """
        
        try:
            app = create_app()
            with app.app_context():
                for book in books:
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

    def get_all_books(self):
        """
        Retrieve all books from the database.

        :return: List of Book objects.
        """
        try:
            return Book.query.all()
        except Exception as e:
            print(f"Error while retrieving books: {e}")
            return []

    def get_book_by_title(self, title):
        """
        Retrieve a single book by its title.

        :param title: Title of the book to retrieve.
        :return: Book object or None if not found.
        """
        try:
            return Book.query.filter_by(title=title).first()
        except Exception as e:
            print(f"Error while retrieving book by title: {e}")
            return None
