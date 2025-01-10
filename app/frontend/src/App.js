import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import BookDetails from './components/BookDetails';

const App = () => {
    return (
        <Router>
     
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/book/:id" element={<BookDetails />} />
            </Routes>
         
        </Router>
    );
};

export default App;
