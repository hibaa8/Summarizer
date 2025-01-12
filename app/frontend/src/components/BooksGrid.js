import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/BooksGrid.css';

const BooksGrid = ({ books }) => {
    const truncateText = (text, maxLength) => {
        if (text.length > maxLength) {
            return text.substring(0, maxLength) + "...";
        }
        return text;
    };

    if (books.length === 0) {
        return <p>No books available to display. Try adjusting your filters or search terms.</p>;
    }

    return (
        <div className="book-grid">
            {books.map((book) => (
                 <Link to={`/book/${book.id}`} key={book.id} className="book-card-link">
                <div className="book-card" key={book.id}>
                    {book.image_url && <img src={book.image_url} alt={book.title} />}
                    <h3>{truncateText(book.title, 50)}</h3>
                    <p>{truncateText(book.author, 30)}</p>
                </div>
                </Link>
            ))}
        </div>
    );
};

export default BooksGrid;
