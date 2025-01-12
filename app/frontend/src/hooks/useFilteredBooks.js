import { useState, useEffect } from 'react';
import Fuse from 'fuse.js';

export const useFilteredBooks = (books, popularCategories) => {
    const [filteredBooks, setFilteredBooks] = useState([]);
    const [selectedFilters, setSelectedFilters] = useState([]);

    useEffect(() => {
        setFilteredBooks(books); // Initialize filteredBooks with the full list of books
    }, [books]);

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
                  return !categories.some((cat) =>
                      popularCategories.some((filterCategory) =>
                          cat.includes(filterCategory.toLowerCase()) ||
                          fuse.search(cat).some((result) => result.item.toLowerCase() === filterCategory.toLowerCase())
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
    };

    return { filteredBooks, selectedFilters, handleFilter };
};
