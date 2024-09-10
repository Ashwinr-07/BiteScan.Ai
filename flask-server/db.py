import psycopg2

# Database connection details
host = "localhost"
port = "5433"
database = "typeface"
user = "postgres"
password = "aryan2008"

# Function to connect to the PostgreSQL database
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        return connection
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        return None
