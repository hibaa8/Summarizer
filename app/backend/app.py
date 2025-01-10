from flask import Flask, jsonify, request, send_from_directory
from init import create_app, db
from models import Book
import os


app = create_app()


@app.route('/api/books', methods=['GET'])
def get_books():
    """
    API endpoint to fetch books, with optional filtering by category (subject).
    """
    subject = request.args.get('subject')
    query = Book.query
    if subject:
        query = query.filter(Book.subject.contains(subject))
    books = query.all()
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

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book_details(book_id):
    """
    API endpoint to fetch details of a specific book by its ID.
    """
    book = Book.query.get_or_404(book_id) 
    book_data = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "language": book.language,
        "subject": book.subject,
        "image_url": book.image_url,
        "amazon_url": book.amazon_url,
        "summary": book.summary,
    }
    return jsonify(book_data)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    """
    Serve the React frontend. Defaults to index.html for all routes not starting with /api.
    """
    react_build_dir = os.path.join(os.path.dirname(__file__), "../frontend/build")
    if path != "" and os.path.exists(os.path.join(react_build_dir, path)):
        return send_from_directory(react_build_dir, path)
    else:
        return send_from_directory(react_build_dir, "index.html")


if __name__ == "__main__":
    app.run(debug=True)
