from flask import Flask, request, jsonify
from restaurant_services import get_restaurant_by_id, get_paginated_restaurants_with_filters, get_restaurants_by_image_search

app = Flask(__name__)

# API route to search for a restaurant by Restaurant ID
@app.route('/restaurant_id/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    return get_restaurant_by_id(restaurant_id)


# API route for paginated restaurant search with filters (radius, cuisine, average spend)
@app.route('/restaurants-paginated', methods=['GET'])
def get_paginated_restaurants():
    return get_paginated_restaurants_with_filters(request)


# API route for image-based restaurant search with pagination
@app.route('/restaurants-by-image', methods=['POST'])
def get_restaurants_by_image():
    # The `get_restaurants_by_image_search` function now handles the entire process, including
    # image upload, cuisine detection via `run_chatgpt`, and paginated search.
    return get_restaurants_by_image_search(request)


# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
