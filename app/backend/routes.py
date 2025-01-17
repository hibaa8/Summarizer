import os
from flask import request, Blueprint, send_from_directory
from .database.db_handler import DatabaseHandler
import os

db_handler = DatabaseHandler()
routes = Blueprint('views', __name__)

@routes.route("/", defaults={"path": ""})
@routes.route("/<path:path>")
def serve_react(path):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    react_build_dir = os.path.join(base_dir, "../frontend/build")
    if path != "" and os.path.exists(os.path.join(react_build_dir, path)):
        return send_from_directory(react_build_dir, path)
    else:
        return send_from_directory(react_build_dir, "index.html")

@routes.route('/api/books', methods=['GET'])
def get_books():
    subject = request.args.get('subject')
    return db_handler.get_all_books(subject)
        

@routes.route('/api/books/<int:book_id>', methods=['GET'])
def get_book_details(book_id):
    return db_handler.get_book_by_id(book_id)
