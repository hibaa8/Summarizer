import React from 'react';
import '../styles/Navbar.css';


const Navbar = () => {
    return (
        <div className="navbar">
            <a href="/" id="navbar-h1-a"><h1>Book Summarizer</h1></a>
            <nav>
                <a href="/">Home</a>
            </nav>
        </div>
    );
};

export default Navbar;
