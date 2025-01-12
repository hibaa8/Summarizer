import React, { useState } from 'react';
import { popularCategories } from '../constants';
import '../styles/Filters.css';

const Filters = ({ onFilter }) => {
    const [selectedCategories, setSelectedCategories] = useState([]);

    const handleCategoryChange = (category) => {
        const updatedCategories = selectedCategories.includes(category)
            ? selectedCategories.filter((c) => c !== category)
            : [...selectedCategories, category];

        setSelectedCategories(updatedCategories);
        onFilter(updatedCategories);
    };

    return (
        <aside className="filters">
            <h3>Filter by Category</h3>
            {popularCategories.sort().map((category) => (
                <div key={category} className="filter-item">
                    <input
                        type="checkbox"
                        id={category}
                        value={category}
                        onChange={() => handleCategoryChange(category.toLowerCase())}
                    />
                    <label htmlFor={category}>{category}</label>
                </div>
            ))}
        </aside>
    );
};

export default Filters;
