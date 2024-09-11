import psycopg2

# Database connection details
host = "localhost"
port = "5433"
database = "Database Name"
user = "Username"
password = "Password"

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
