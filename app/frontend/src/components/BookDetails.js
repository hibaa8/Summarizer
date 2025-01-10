import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import '../styles/BookDetails.css';
import Navbar from "./Navbar"

const BookDetails = () => {
    const { id } = useParams();
    const [book, setBook] = useState(null);

    useEffect(() => {
        axios.get(`/api/books/${id}`)
        .then((response) => {
            const data = response.data;
            if (data.summary) {
                data.summary = data.summary
                    .replace(/```html/g, "") 
                    .replace(/```/g, "");  
            }
            setBook(data);
        })
        .catch((error) => console.error('Error fetching book details:', error));
}, [id]);

    if (!book) {
        return <p>Loading...</p>;
    }

    return (
        <div>
           <Navbar></Navbar>
            <div className="book-details-container">
                <h1 className="book-details-title">{book.title}</h1>
                <div className="book-metadata">
                    <p><strong>Author:</strong> {book.author}</p>
                    <p><strong>Language:</strong> {book.language}</p>
                    <p><strong>Subject:</strong> {book.subject}</p>
                </div>
                {book.image_url && (
                    <img
                        className="book-details-image"
                        src={book.image_url}
                        alt={book.title}
                    />
                )}
                {book.amazon_url && (
                <a
                    className="amazon-link"x
                    href={book.amazon_url}
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Buy on Amazon
                </a>
                )}
                <div
                    className="book-summary"
                    dangerouslySetInnerHTML={{ __html: book.summary }}
                />
                <div className="back-home">
                    <Link to="/">Back to Home</Link>
                </div>
            </div>
        </div>
    );
};

export default BookDetails;
