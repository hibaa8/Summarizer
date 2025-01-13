import { useState, useEffect } from 'react';

export const useSearchBooks = (filteredBooks) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);

    useEffect(() => {
        if (!searchQuery) {
            setSearchResults(filteredBooks); 
            return;
        }

        const searchWords = searchQuery.toLowerCase().split(/\s+/);

        const exactMatches = filteredBooks.filter((book) => {
            const searchableFields = [
                book.title?.toLowerCase(),
                book.author?.toLowerCase(),
                book.language?.toLowerCase(),
                book.subject?.toLowerCase(),
            ];

            return searchableFields.some((field) =>
                field?.includes(searchQuery.toLowerCase())
            );
        });

        if (exactMatches.length > 0) {
            setSearchResults(exactMatches);
            return;
        }

        const searchResults = filteredBooks
            .map((book) => {
                let weight = 0;

                if (book.title?.toLowerCase().includes(searchQuery)) {
                    weight += 5;
                }
                if (book.author?.toLowerCase().includes(searchQuery)) {
                    weight += 4;
                }
                if (
                    searchWords.some((word) =>
                        book.language?.toLowerCase().includes(word)
                    )
                ) {
                    weight += 3;
                }
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
            .sort((a, b) => b.weight - a.weight)
            .map((entry) => entry.book);

        setSearchResults(searchResults);
    }, [searchQuery, filteredBooks]);

    const handleSearch = (query) => {
        setSearchQuery(query.toLowerCase());
    };

    return { searchQuery, searchResults, handleSearch };
};
