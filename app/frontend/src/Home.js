import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Filters from './components/Filters';
import BooksGrid from './components/BooksGrid';
import "./styles/Home.css"


const Home = () => {
    const [books, setBooks] = useState([]); // All books from the backend
    const [filteredBooks, setFilteredBooks] = useState([]); 
    const [displayedBooks, setDisplayedBooks] = useState([]); 
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedFilters, setSelectedFilters] = useState([]);

    useEffect(() => {
        // Fetch all books from the backend
        axios.get('/api/books')
            .then((response) => {
                setBooks(response.data);
                setFilteredBooks(response.data); 
                setDisplayedBooks(response.data); 
            })
            .catch((error) => console.error('Error fetching books:', error));
    }, []);

    const handleFilter = (selectedCategories) => {
        setSelectedFilters(selectedCategories);

        const filtered = selectedCategories.length
            ? books.filter((book) =>
                  book.subject
                      ?.split(',')
                      .map((cat) => cat.trim().toLowerCase())
                      .some((cat) => selectedCategories.includes(cat))
              )
            : books;

        setFilteredBooks(filtered);
        setDisplayedBooks(
            filtered.filter((book) =>
                searchQuery
                    ? book.title.toLowerCase().includes(searchQuery) ||
                      book.author.toLowerCase().includes(searchQuery)
                    : true
            )
        ); 
    };

    const handleSearch = (query) => {
        setSearchQuery(query.toLowerCase());
        const searchResults = filteredBooks.filter(
            (book) =>
                book.title.toLowerCase().includes(query.toLowerCase()) ||
                book.author.toLowerCase().includes(query.toLowerCase())
        );
        setDisplayedBooks(searchResults);
    };

    return (
        <div>
            <Navbar />
            <div className="search-bar">
                <input
                    type="text"
                    placeholder="Search by title or author..."
                    value={searchQuery}
                    onChange={(e) => handleSearch(e.target.value)}
                />
            </div>
            <div className="content">
                <Filters books={books} onFilter={handleFilter} />
                <BooksGrid books={displayedBooks} />
            </div>
        </div>
    );
};

export default Home;
