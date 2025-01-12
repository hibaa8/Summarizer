import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Filters from './components/Filters';
import BooksGrid from './components/BooksGrid';
import SearchBar from './components/SearchBar';
import { useFilteredBooks } from './hooks/useFilteredBooks';
import { useSearchBooks } from './hooks/useSearchBooks';
import { popularCategories } from './constants';
import "./styles/Home.css";

const Home = () => {
    const [books, setBooks] = useState([]);
    const { filteredBooks, selectedFilters, handleFilter } = useFilteredBooks(books, popularCategories);
    const { searchQuery, searchResults, handleSearch } = useSearchBooks(filteredBooks);

    useEffect(() => {
        axios.get('/api/books')
            .then((response) => {
                setBooks(response.data);
            })
            .catch((error) => console.error('Error fetching books:', error));
    }, []);

    return (
        <div>
            <Navbar />
            <SearchBar query={searchQuery} onSearch={handleSearch} />
            <div className="content">
                <Filters selectedFilters={selectedFilters} onFilter={handleFilter} />
                <BooksGrid books={searchResults} />
            </div>
        </div>
    );
};

export default Home;
