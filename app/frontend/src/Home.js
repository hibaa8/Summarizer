import React, { useEffect, useState } from 'react';
import Fuse from 'fuse.js';
import axios from 'axios';
import Navbar from './components/Navbar';
import Filters from './components/Filters';
import BooksGrid from './components/BooksGrid';
import SearchBar from './components/SearchBar';
import { popularCategories } from './constants';
import "./styles/Home.css"


const Home = () => {
    const [books, setBooks] = useState([]); 
    const [filteredBooks, setFilteredBooks] = useState([]); 
    const [displayedBooks, setDisplayedBooks] = useState([]); 
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedFilters, setSelectedFilters] = useState([]);

    useEffect(() => {
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
    
        const popularCategoriesLowercase = popularCategories
            .filter((category) => category.toLowerCase() !== 'other') 
            .map((category) => category.toLowerCase());

        const fuse = new Fuse(popularCategoriesLowercase, {
            includeScore: true, 
            threshold: 0.3,     
        });

        const filtered = selectedCategories.includes('other')
        ? books.filter((book) => {
              const categories = book.subject
                  ?.split(',')
                  .map((cat) => cat.trim().toLowerCase());
              return (
                  !categories.some((cat) =>
                      popularCategories.some((filterCategory) =>
                          cat.includes(filterCategory.toLowerCase())||
                          fuse.search(cat).some((result) => result.item.toLowerCase() === filterCategory.toLowerCase())
                      )
                  )
              );
          })
        : selectedCategories.length
        ? books.filter((book) => {
              const categories = book.subject
                  ?.split(',')
                  .map((cat) => cat.trim().toLowerCase());
              return categories.some((cat) =>
                  selectedCategories.some((filterCategory) =>
                      cat.includes(filterCategory.toLowerCase()) ||
                      fuse.search(cat).some((result) => result.item.toLowerCase() === filterCategory.toLowerCase())
                  )
              );
          })
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
        const searchWords = query.toLowerCase().split(/\s+/); 
    
        const exactMatches = filteredBooks.filter((book) => {
            const searchableFields = [
                book.title?.toLowerCase(),
                book.author?.toLowerCase(),
                book.language?.toLowerCase(),
                book.subject?.toLowerCase(),
            ];
    
            return searchableFields.some((field) => field?.includes(query.toLowerCase()));
        });
    
        // If there are exact matches, only display those
        if (exactMatches.length > 0) {
            setDisplayedBooks(exactMatches);
            return;
        }
    
        // Fallback to weighted search logic if no exact matches
        const searchResults = filteredBooks
            .map((book) => {
                let weight = 0;
    
                const searchableFields = [
                    book.title?.toLowerCase(),
                    book.author?.toLowerCase(),
                    book.language?.toLowerCase(),
                    book.subject?.toLowerCase(),
                ].join(' ');
    
                // Partial match in title
                if (book.title?.toLowerCase().includes(query.toLowerCase())) {
                    weight += 5;
                }
    
                // Partial match in author
                if (book.author?.toLowerCase().includes(query.toLowerCase())) {
                    weight += 4;
                }
    
                // Match in language
                if (
                    searchWords.some((word) =>
                        book.language?.toLowerCase().includes(word)
                    )
                ) {
                    weight += 3;
                }
    
                // Match in subjects (substring match for each word)
                if (
                    book.subject
                        ?.toLowerCase()
                        .split(',')
                        .some((subject) =>
                            searchWords.some((word) =>
                                subject.trim().includes(word)
                            )
                        )
                ) {
                    weight += 2;
                }
    
                return { book, weight };
            })
            .filter((entry) => entry.weight > 0) 
            .sort((a, b) => b.weight - a.weight) // Sort by weight in descending order
            .map((entry) => entry.book); 
    
        setDisplayedBooks(searchResults);
    };
    
    
    

    return (
        <div>
            <Navbar />
            <SearchBar query={searchQuery} onSearch={handleSearch} />
            <div className="content">
                <Filters books={books} onFilter={handleFilter} />
                <BooksGrid books={displayedBooks} />
            </div>
        </div>
    );
};

export default Home;


