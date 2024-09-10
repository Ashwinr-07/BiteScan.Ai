import React from 'react';
import RestaurantSearchByID from './RestaurantSearchByID';
import RestaurantSearchByImage from './RestaurantSearchByImage';
import RestaurantSearchWithFilters from './RestaurantSearchWithFilters';

import './App.css';

function Header() {
  return (
    <header className="top-header">
      <div className="logo-container">
        <img src="/logo.png" alt="BiteScan.AI Logo" className="logo-image" />
        <span className="logo-text">BiteScan.AI</span>
      </div>
    </header>
  );
}

function App() {
  return (
    <div className="app-container">
      <Header />
      <main className="main-container">
        <div className="content-wrapper">
          <h1 className="main-heading">Discover the best food.</h1>
          <h2 className="sub-heading">Snap, Search, Savor – Find Your Meal Match Instantly!</h2>
          <div className="dotted-line"></div>
          <RestaurantSearchByID />
          <div className="dotted-line"></div>
          <RestaurantSearchByImage />
          <div className="dotted-line"></div>
          <RestaurantSearchWithFilters />
        </div>
      </main>
    </div>
  );
}

export default App;