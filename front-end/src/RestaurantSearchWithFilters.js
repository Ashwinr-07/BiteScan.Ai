import React, { useState } from 'react';
import axios from 'axios';
import './RestaurantSearchWithFilters.css';

const cuisinesList = ['BBQ', 'Thai', 'North Indian', 'South Indian', 'Cafe', 'Breakfast', 'Mughlai', 'Arabic', 'Pizza', 'German', 'Italian', 'IceCream', 'Dessert', 'Mexican', 'Asian', 'Caribbean', 'Seafood', 'Japanese'];

const RestaurantSearchWithFilters = () => {
    const [filters, setFilters] = useState({
        latitude: '',
        longitude: '',
        radius: 7,
        cuisine: '',
        averageSpend: 200
    });
    const [restaurants, setRestaurants] = useState([]);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [selectedRestaurant, setSelectedRestaurant] = useState(null); // State for the selected restaurant

    const fetchRestaurants = (newPage = 1) => {
        axios.get(`/restaurants-paginated`, {
            params: {
                latitude: filters.latitude,
                longitude: filters.longitude,
                radius: filters.radius,
                cuisine: filters.cuisine,
                average_cost_for_two: filters.averageSpend,
                page: newPage
            }
        })
            .then(response => {
                setRestaurants(response.data.restaurants || []);
                setTotalPages(response.data.total_pages || 1); // Set total pages from response
                setPage(newPage); // Update current page
            })
            .catch(error => console.error(error));
    };

    const handlePageChange = (newPage) => {
        fetchRestaurants(newPage); // Fetch data for the selected page
    };

    const renderPagination = () => {
        return (
            <div className="pagination-container">
                {Array.from({ length: totalPages }, (_, i) => (
                    <div
                        key={i}
                        className={`pagination-box ${page === i + 1 ? 'active' : ''}`}
                        onClick={() => handlePageChange(i + 1)}
                    ></div>
                ))}
            </div>
        );
    };

    // Function to select and show detailed restaurant information
    const handleRestaurantClick = (restaurant) => {
        setSelectedRestaurant(restaurant); // Show detailed info
    };

    // Function to close the modal or detailed view
    const closeModal = () => {
        setSelectedRestaurant(null);
    };

    return (
        <div className="restaurant-search-with-filters">
            <h1 className="grey-heading">More Filtering!!</h1>

            {/* Cuisine Nav Bar */}
            <div className="cuisine-nav-bar">
                {cuisinesList.map(cuisine => (
                    <div
                        key={cuisine}
                        className={`cuisine-box ${filters.cuisine === cuisine ? 'selected' : ''}`}
                        onClick={() => setFilters({ ...filters, cuisine })}
                    >
                        {cuisine}
                    </div>
                ))}
            </div>

            {/* Latitude, Longitude, Radius, and Average Spend Input */}
            <div className="location-inputs-container">
                <input
                    type="text"
                    value={filters.latitude}
                    onChange={(e) => setFilters({ ...filters, latitude: e.target.value })}
                    placeholder="Enter latitude"
                    className="input-field"
                />
                <input
                    type="text"
                    value={filters.longitude}
                    onChange={(e) => setFilters({ ...filters, longitude: e.target.value })}
                    placeholder="Enter longitude"
                    className="input-field"
                />
                <input
                    type="text"
                    value={filters.radius}
                    onChange={(e) => setFilters({ ...filters, radius: e.target.value })}
                    placeholder="Enter radius in kms"
                    className="input-field"
                />
            </div>

            <div className="range-input-container">
                <label>Average Spend: ₹{filters.averageSpend}</label>
                <input
                    type="range"
                    min="200"
                    max="5000"
                    value={filters.averageSpend}
                    onChange={(e) => setFilters({ ...filters, averageSpend: e.target.value })}
                    className="range-slider"
                />
            </div>

            {/* Search Button */}
            <div className="button-container">
                <button className="search-button" onClick={() => fetchRestaurants(1)}>
                    Search
                </button>
            </div>

            {/* Display Restaurants */}
            {restaurants.length > 0 && (
                <div className="restaurant-boxes">
                    {restaurants.map((restaurant) => (
                        <div key={restaurant.restaurant_id} className="restaurant-box" onClick={() => handleRestaurantClick(restaurant)}>
                            {restaurant.restaurant_name}
                        </div>
                    ))}
                </div>
            )}

            {/* Pagination */}
            {restaurants.length > 0 && totalPages > 1 && renderPagination()}

            {/* Modal/Detailed View for Selected Restaurant */}
            {selectedRestaurant && (
                <div className="restaurant-modal">
                    <div className="modal-content">
                        <h2>{selectedRestaurant.restaurant_name}</h2>
                        <p><strong>Cuisines:</strong> {selectedRestaurant.cuisines}</p>
                        <p><strong>Average Cost for Two:</strong> {selectedRestaurant.average_cost_for_two}</p>
                        <p><strong>Location:</strong> {selectedRestaurant.latitude}, {selectedRestaurant.longitude}</p>
                        <button className="close-button" onClick={closeModal}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default RestaurantSearchWithFilters;
