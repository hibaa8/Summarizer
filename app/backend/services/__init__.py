from backend.database.db_handler import DatabaseHandler
from flask import request

db_handler = DatabaseHandler()

def setup_routes(app):
    @app.route('/api/books', methods=['GET'])
    def get_books():
        subject = request.args.get('subject')
        return db_handler.get_all_books(subject)
        

    @app.route('/api/books/<int:book_id>', methods=['GET'])
    def get_book_details(book_id):
        return db_handler.get_book_by_id(book_id)
      
