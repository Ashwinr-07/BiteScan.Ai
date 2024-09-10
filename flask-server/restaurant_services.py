from flask import jsonify, request
from haversine import haversine, Unit
from db import get_db_connection
from cuisine import run_chatgpt
from fuzzywuzzy import fuzz

# Function to get restaurant by ID
def get_restaurant_by_id(restaurant_id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor()
    query = "SELECT * FROM zomato_restaurants WHERE restaurant_id = %s;"
    cursor.execute(query, (restaurant_id,))
    restaurant = cursor.fetchone()
    
    if restaurant:
        restaurant_data = {
            'restaurant_id': restaurant[0],
            'restaurant_name': restaurant[1],
            'country_code': restaurant[2],
            'city': restaurant[3],
            'address': restaurant[4],
            'locality': restaurant[5],
            'locality_verbose': restaurant[6],
            'longitude': restaurant[7],
            'latitude': restaurant[8],
            'cuisines': restaurant[9],
            'average_cost_for_two': restaurant[10],
            'currency': restaurant[11],
            'has_table_booking': restaurant[12],
            'has_online_delivery': restaurant[13],
            'is_delivering_now': restaurant[14],
            'switch_to_order_menu': restaurant[15],
            'price_range': restaurant[16],
            'aggregate_rating': restaurant[17],
            'rating_color': restaurant[18],
            'rating_text': restaurant[19],
            'votes': restaurant[20]
        }
        return jsonify(restaurant_data), 200
    else:
        return jsonify({'error': 'Restaurant not found'}), 404


# List of possible cuisines for fuzzy matching
cuisines_list = ['BBQ', 'Thai', 'North Indian', 'South Indian', 'Cafe', 'Breakfast', 'Mughlai', 'Arabic', 'Pizza', 'German', 'Italian', 'IceCream', 'Dessert', 'Mexican', 'Asian', 'Caribbean', 'Seafood', 'Japanese']

# Function to get paginated restaurants with filters (radius, cuisine, average spend, image search)
def get_paginated_restaurants_with_filters(request):
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        page = int(request.args.get('page', 1))  # Default to page 1
        page_size = 9  # 9 items per page
        offset = (page - 1) * page_size

        if page > 9:
            return jsonify({
                'restaurants': [],
                'page': page,
                'total_pages': 9  # Total pages capped at 9
            }), 200
        
        # Optional filters
        radius_km = float(request.args.get('radius', 7))  # Radius (default to 7km)
        cuisine_filter = request.args.get('cuisine')  # Cuisine filter from list
        max_average_spend = request.args.get('average_cost_for_two')  # Filter by average spend

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    user_location = (latitude, longitude)

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor()

    # Base query for fetching restaurants within a certain radius
    query = """
    SELECT restaurant_id, restaurant_name, cuisines, average_cost_for_two, latitude, longitude 
    FROM zomato_restaurants
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """
    
    # Add cuisine filtering if a cuisine filter is provided
    if cuisine_filter:
        query += f" AND cuisines ILIKE '%{cuisine_filter}%'"

    # Add average spend filtering if provided
    if max_average_spend:
        query += f" AND average_cost_for_two <= {max_average_spend}"

    cursor.execute(query)
    restaurants = cursor.fetchall()

    # Use fuzzy matching for cuisine filter
    filtered_restaurants = []
    for restaurant in restaurants:
        restaurant_location = (restaurant[4], restaurant[5])  # (latitude, longitude)
        distance = haversine(user_location, restaurant_location, unit=Unit.KILOMETERS)
        
        if distance <= radius_km:
            # If fuzzy cuisine filter is provided, perform fuzzy match
            if cuisine_filter:
                if fuzz.partial_ratio(cuisine_filter.lower(), restaurant[2].lower()) > 70:
                    filtered_restaurants.append({
                        'restaurant_id': restaurant[0],
                        'restaurant_name': restaurant[1],
                        'cuisines': restaurant[2],
                        'average_cost_for_two': restaurant[3],
                        'latitude': restaurant[4],
                        'longitude': restaurant[5],
                        'distance_km': distance
                    })
            else:
                filtered_restaurants.append({
                    'restaurant_id': restaurant[0],
                    'restaurant_name': restaurant[1],
                    'cuisines': restaurant[2],
                    'average_cost_for_two': restaurant[3],
                    'latitude': restaurant[4],
                    'longitude': restaurant[5],
                    'distance_km': distance
                })

    # Pagination
    paginated_restaurants = filtered_restaurants[offset:offset + page_size]

    cursor.close()
    connection.close()

    if paginated_restaurants:
        return jsonify({
            'restaurants': paginated_restaurants,
            'page': page,
            'total_pages': (len(filtered_restaurants) + page_size - 1) // page_size  # Total pages logic
        }), 200
    else:
        return jsonify({'message': 'No restaurants found with the applied filters.'}), 404
    



def get_restaurants_by_image_search(request):
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        page = int(request.args.get('page', 1))  # Default to page 1
        page_size = 9  # 9 items per page
        offset = (page - 1) * page_size
        radius_km = float(request.args.get('radius', 7))  # Default radius 7km

        if page > 9:
            return jsonify({
                'restaurants': [],
                'page': page,
                'total_pages': 9  # Total pages capped at 9
            }), 200

        # Ensure an image file is provided
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']
        image_path = "temp_image.png"  # Temporary location for the image
        image_file.save(image_path)

        # Detect the cuisine using the run_chatgpt function
        cuisine_filter = run_chatgpt(image_path)

        if not cuisine_filter:
            return jsonify({"error": "Cuisine could not be identified"}), 500

        print(f"Detected cuisine: {cuisine_filter}")  # Debugging print

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    user_location = (latitude, longitude)

    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor()

    # Query to search for restaurants based on the detected cuisine
    query = """
    SELECT restaurant_id, restaurant_name, cuisines, average_cost_for_two, latitude, longitude 
    FROM zomato_restaurants
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    AND cuisines ILIKE %s
    """
    cursor.execute(query, (f"%{cuisine_filter}%",))
    restaurants = cursor.fetchall()

    # Filter by radius
    filtered_restaurants = []
    for restaurant in restaurants:
        restaurant_location = (restaurant[4], restaurant[5])  # (latitude, longitude)
        distance = haversine(user_location, restaurant_location, unit=Unit.KILOMETERS)

        if distance <= radius_km:
            filtered_restaurants.append({
                'restaurant_id': restaurant[0],
                'restaurant_name': restaurant[1],
                'cuisines': restaurant[2],
                'average_cost_for_two': restaurant[3],
                'latitude': restaurant[4],
                'longitude': restaurant[5],
                'distance_km': distance
            })

    # Pagination
    paginated_restaurants = filtered_restaurants[offset:offset + page_size]

    cursor.close()
    connection.close()

    if paginated_restaurants:
        return jsonify({
            'restaurants': paginated_restaurants,
            'page': page,
            'total_pages': (len(filtered_restaurants) + page_size - 1) // page_size  # Total pages logic
        }), 200
    else:
        return jsonify({'message': 'No restaurants found for the detected cuisine within the radius.'}), 404