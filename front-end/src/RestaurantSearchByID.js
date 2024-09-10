import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './RestaurantSearchByID.css';

// Import images
import gemini1 from './assets/gemini1.png';
import gemini2 from './assets/gemini2.png';
import gemini3 from './assets/gemini3.png';

const RestaurantSearchByID = () => {
    const [restaurantID, setRestaurantID] = useState('');
    const [restaurant, setRestaurant] = useState(null);
    const [error, setError] = useState('');
    const [randomImage, setRandomImage] = useState('');

    // Randomly select an image from gemini1, gemini2, gemini3
    useEffect(() => {
        const images = [gemini1, gemini2, gemini3]; // Use the imported images
        const randomIndex = Math.floor(Math.random() * images.length);
        setRandomImage(images[randomIndex]);
    }, []);

    const fetchRestaurant = () => {
        if (restaurantID) {
            axios.get(`/restaurant_id/${restaurantID}`)
                .then(response => {
                    if (response.data.error) {
                        setError('Restaurant not found');
                        setRestaurant(null);
                    } else {
                        setRestaurant(response.data);
                        setError(''); 
                    }
                })
                .catch(error => {
                    console.error(error);
                    setError('An error occurred while fetching the restaurant.');
                });
        } else {
            setError('Please enter a valid restaurant ID.');
        }
    };

    const renderRatingBar = (rating) => {
        const ratingWidth = `${(rating / 5) * 100}%`;
        return <div className="rating-bar-container">
            <div className="rating-bar" style={{ width: ratingWidth }}></div>
        </div>;
    };

    return (
        <div className="restaurant-search-container">
            <div className="search-section">
    <input
        type="number"
        className="input-box"
        value={restaurantID}
        onChange={(e) => setRestaurantID(e.target.value)}
        placeholder="Enter restaurant ID"
    />
    <button className="red-button" onClick={fetchRestaurant}>Find a Restaurant</button>
</div>


            {restaurant && (
                <div className="restaurant-output-section">
                    <div className="restaurant-details-box">
                        <div className="restaurant-info-box">
                            <h2>{restaurant.restaurant_name}</h2>
                            <p><strong>Cuisine:</strong> {restaurant.cuisines}</p>
                            <p><strong>Cost for Two:</strong> {restaurant.currency} {restaurant.average_cost_for_two}</p>
                            <p><strong>ID:</strong> {restaurant.restaurant_id}</p>
                            <p><strong>Votes:</strong> 👍 {restaurant.votes}</p>
                            <div className="rating-section">
                                <p><strong>Rating:</strong> {restaurant.aggregate_rating} ({restaurant.rating_text})</p>
                                {renderRatingBar(restaurant.aggregate_rating)}
                            </div>
                            {!restaurant.has_online_delivery && <p className="closed-status">Closed</p>}
                        </div>
                    </div>

                    {/* Display the image using random selection */}
                    <div className="image-section" style={{ backgroundImage: `url(${randomImage})` }}>
                    </div>
                </div>
            )}

            {error && <div className="restaurant-result">{error}</div>}
        </div>
    );
};

export default RestaurantSearchByID;
