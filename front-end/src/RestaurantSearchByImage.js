import React, { useState } from 'react';
import axios from 'axios';
import './RestaurantSearchByImage.css';

const RestaurantSearchByImage = () => {
    const [file, setFile] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);
    const [latitude, setLatitude] = useState('');
    const [longitude, setLongitude] = useState('');
    const [radius, setRadius] = useState('');
    const [restaurants, setRestaurants] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const pageSize = 9;

    const [selectedRestaurant, setSelectedRestaurant] = useState(null); // State to hold selected restaurant

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFile(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const resetImageUpload = () => {
        setFile(null);
        setImagePreview(null);
        setRestaurants([]);
        setPage(1);
        setSelectedRestaurant(null); // Reset selected restaurant
    };

    const uploadImage = (newPage = 1) => {
        if (!file) {
            setError('Please upload an image file.');
            return;
        }

        const formData = new FormData();
        formData.append('image', file);
        formData.append('latitude', latitude);
        formData.append('longitude', longitude);
        formData.append('radius', radius);

        setLoading(true);

        axios.post(`/restaurants-by-image?latitude=${latitude}&longitude=${longitude}&radius=${radius}&page=${newPage}`, formData)
            .then(response => {
                setRestaurants(response.data.restaurants || []);
                setTotalPages(response.data.total_pages || 1);
                setPage(newPage);
                setError(null);
            })
            .catch(() => setError('Error uploading image'))
            .finally(() => setLoading(false));
    };

    const handlePageChange = (newPage) => {
        uploadImage(newPage);
    };

    const handleRestaurantClick = (restaurant) => {
        setSelectedRestaurant(restaurant); // Set selected restaurant to display in modal
    };

    const closeRestaurantDetails = () => {
        setSelectedRestaurant(null); // Close restaurant details
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

    return (
        <div className="restaurant-search-by-image">
            <h1 className="typing-text">Search by what you see!</h1>

            <div className="location-inputs-container">
                <div className="input-container red-box">
                    <input
                        type="text"
                        value={latitude}
                        onChange={(e) => setLatitude(e.target.value)}
                        placeholder="Enter latitude"
                        className="input-field"
                    />
                </div>
                <div className="input-container white-box">
                    <input
                        type="text"
                        value={longitude}
                        onChange={(e) => setLongitude(e.target.value)}
                        placeholder="Enter longitude"
                        className="input-field"
                    />
                </div>
                <div className="input-container red-box">
                    <input
                        type="text"
                        value={radius}
                        onChange={(e) => setRadius(e.target.value)}
                        placeholder="Enter radius in kms"
                        className="input-field"
                    />
                </div>
            </div>

            <div className="image-upload-container">
                {!imagePreview && (
                    <>
                        <h2>Upload Your Image</h2>
                        <input
                            type="file"
                            onChange={handleImageUpload}
                            className="input-field"
                        />
                    </>
                )}

                {imagePreview && (
                    <div className="image-preview-container">
                        <img src={imagePreview} alt="Uploaded Preview" className="image-preview" />
                    </div>
                )}
            </div>

            <div className="button-container">
                <button className="search-button" onClick={() => uploadImage(1)}>
                    Search
                </button>
                {imagePreview && (
                    <button className="new-image-button" onClick={resetImageUpload}>
                        New Image
                    </button>
                )}
            </div>

            {loading && <p className="loading-text">Loading...</p>}

            {restaurants.length > 0 && !loading && (
                <div className="restaurant-boxes">
                    {restaurants.map((restaurant) => (
                        <div
                            key={restaurant.restaurant_id}
                            className="restaurant-box"
                            onClick={() => handleRestaurantClick(restaurant)}
                        >
                            {restaurant.restaurant_name}
                        </div>
                    ))}
                </div>
            )}

            {!loading && restaurants.length > 0 && totalPages > 1 && renderPagination()}

            {selectedRestaurant && (
                <div className="restaurant-detail-overlay">
                    <div className="restaurant-detail-card">
                        <button className="close-button" onClick={closeRestaurantDetails}>×</button>
                        <h2>{selectedRestaurant.restaurant_name}</h2>
                        <p><span className="highlight">Cuisine:</span> {selectedRestaurant.cuisines}</p>
                        <p><span className="highlight">Cost for Two:</span> {selectedRestaurant.currency} {selectedRestaurant.average_cost_for_two}</p>
                        
                    </div>
                </div>
            )}

            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default RestaurantSearchByImage;
