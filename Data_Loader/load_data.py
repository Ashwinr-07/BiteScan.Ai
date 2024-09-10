import pandas as pd
import psycopg2
from psycopg2 import sql

# Database connection details
host = "localhost"
port = "5433"
database = "username"  # Your database name
user = "postgres"
password = "password"

# Load the CSV file with explicit encoding
csv_file_path = "zomato.csv"
try:
    data = pd.read_csv(csv_file_path, encoding='ISO-8859-1')  # Change encoding if needed
    print("CSV file loaded successfully.")
except FileNotFoundError as fnf_error:
    print(f"Error: {fnf_error}")
    exit()
except UnicodeDecodeError as decode_error:
    print(f"Error loading CSV file due to encoding issue: {decode_error}")
    exit()
except Exception as csv_error:
    print(f"Error loading CSV file: {csv_error}")
    exit()

# Convert 'Yes'/'No' to boolean (True/False)
boolean_columns = ['Has Table booking', 'Has Online delivery', 'Is delivering now', 'Switch to order menu']
for col in boolean_columns:
    data[col] = data[col].map({'Yes': True, 'No': False})

# Establish a connection to the database
try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    cursor = connection.cursor()
    print("Database connection successful.")
    
    # Create the table if it doesn't exist
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS zomato_restaurants (
        restaurant_id BIGINT PRIMARY KEY,
        restaurant_name VARCHAR(255),
        country_code INT,
        city VARCHAR(255),
        address TEXT,
        locality VARCHAR(255),
        locality_verbose VARCHAR(255),
        longitude FLOAT,
        latitude FLOAT,
        cuisines TEXT,
        average_cost_for_two INT,
        currency VARCHAR(50),
        has_table_booking BOOLEAN,
        has_online_delivery BOOLEAN,
        is_delivering_now BOOLEAN,
        switch_to_order_menu BOOLEAN,
        price_range INT,
        aggregate_rating FLOAT,
        rating_color VARCHAR(50),
        rating_text VARCHAR(50),
        votes INT
    );
    '''
    cursor.execute(create_table_query)
    print("Table check/creation successful.")
    
    # Insert data into the table
    for index, row in data.iterrows():
        try:
            insert_query = sql.SQL('''
                INSERT INTO zomato_restaurants (
                    restaurant_id, restaurant_name, country_code, city, address, locality, 
                    locality_verbose, longitude, latitude, cuisines, average_cost_for_two, 
                    currency, has_table_booking, has_online_delivery, is_delivering_now, 
                    switch_to_order_menu, price_range, aggregate_rating, rating_color, 
                    rating_text, votes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''')
            cursor.execute(insert_query, (
                row['Restaurant ID'], row['Restaurant Name'], row['Country Code'], row['City'], 
                row['Address'], row['Locality'], row['Locality Verbose'], row['Longitude'], 
                row['Latitude'], row['Cuisines'], row['Average Cost for two'], row['Currency'], 
                row['Has Table booking'], row['Has Online delivery'], 
                row['Is delivering now'], row['Switch to order menu'], 
                row['Price range'], row['Aggregate rating'], row['Rating color'], 
                row['Rating text'], row['Votes']
            ))
        except Exception as row_error:
            print(f"Error inserting row {index}: {row_error}")
            continue  # Skip this row and continue with others

    # Commit changes and close connection
    connection.commit()
    cursor.close()
    connection.close()
    print("Data loaded successfully into PostgreSQL.")

except psycopg2.OperationalError as db_error:
    print(f"Error connecting to the database: {db_error}")
except Exception as error:
    print(f"Error loading data: {error}")
