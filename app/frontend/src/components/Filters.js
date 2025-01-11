// import React, { useEffect, useState } from 'react';
// import '../styles/Filters.css';
// const popularCategories = [
//     'Science fiction',
//     'Adventure stories',
//     'Short stories',
//     'Psychological fiction',
//     'Romance',
//     'Domestic fiction',
//     'Conduct of life',
//     'Historical fiction',
//     'Humorous stories',
//     'Horror tales',
//     'Gothic fiction',
//     'Fiction',
//     'Detective and mystery stories',
//     'Children\'s stories',
//     'Ghost stories',
//     'Autobiographical fiction',
//     'Comedies',
//     'Fairy Tales',
//     'War Stories',
//     'Poetry',
//     'Ethics',
//     'Other',
// ];

// const Filters = ({ books, onFilter }) => {
//     const [selectedCategories, setSelectedCategories] = useState([]);

//     const handleCategoryChange = (category) => {
//         const updatedCategories = selectedCategories.includes(category)
//             ? selectedCategories.filter((c) => c !== category) 
//             : [...selectedCategories, category]; 

//         setSelectedCategories(updatedCategories);
//         onFilter(updatedCategories);
//     };

//     return (
//         <aside className="filters">
//             <h3>Filter by Category</h3>
//             {popularCategories.sort().map((category) => (
//                 <div key={category} className="filter-item">
//                     <input
//                         type="checkbox"
//                         id={category}
//                         value={category}
//                         onChange={() => handleCategoryChange(category.toLowerCase())}
//                     />
//                     <label htmlFor={category}>{category}</label>
//                 </div>
//             ))}
//         </aside>
//     );
// };

// export default Filters;

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
