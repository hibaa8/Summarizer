from . import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True, unique=True)
    author = db.Column(db.String(255), nullable=False, index=True)
    language = db.Column(db.String(100), nullable=False, index=True)
    subject = db.Column(db.Text, nullable=True) 
    image_url = db.Column(db.String(255), nullable=True)
    amazon_url = db.Column(db.String(255), nullable=True, unique=True)
    summary = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Book {self.title}>"

