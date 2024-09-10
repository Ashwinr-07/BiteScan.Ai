
<img width="512" alt="image" src="https://github.com/user-attachments/assets/38fc66ec-c0b0-45a8-9820-fe7615ddb40c">


# BiteScan.Ai - Restaurant Listing & Search Application

BiteScan.Ai is a full-stack application that allows users to search for restaurants based on images of food and filter them based on location, cuisine, and average spending. The project leverages a Flask back-end for API management and a React front-end for user interaction.


![Screen Recording 2024-09-10 at 10 14 19 PM](https://github.com/user-attachments/assets/3af97e73-d7c8-453e-9bff-a1a7027e7c78)
---


## Project Structure

```
.
├── Data_Loader
├── README.md
├── flask-server  # Flask (Python) server handling backend
│   ├── app.py
│   └── ...
└── front-end     # React (JavaScript) front-end handling the UI
    ├── src/
    ├── public/
    └── package.json
```

## Prerequisites

Ensure you have the following installed on your system:

- [Node.js](https://nodejs.org/) (for the front-end)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- [Python 3](https://www.python.org/downloads/) (for the Flask server)
- [Flask](https://flask.palletsprojects.com/) (`pip install flask`)

## Setting up the Front-End

1. **Navigate to the `front-end` directory**:

   ```bash
   cd front-end
   ```

2. **Install dependencies**:

   Run the following command to install all the Node.js dependencies listed in `package.json`:

   ```bash
   npm install
   ```

3. **Start the front-end development server**:

   After the installation is complete, you can start the React development server:

   ```bash
   npm start
   ```

   The front-end will now be accessible at `http://localhost:3000`.

## Setting up the Flask Server (Back-End)

1. **Navigate to the `flask-server` directory**:

   ```bash
   cd flask-server
   ```

2. **Install the necessary Python packages**:

   If a `requirements.txt` file exists, you can install the necessary Python packages by running:

   ```bash
   pip install -r requirements.txt
   ```

   Otherwise, install Flask manually using:

   ```bash
   pip install flask
   ```

3. **Run the Flask server**:

   Start the Flask server by running:

   ```bash
   python app.py
   ```

   The back-end server will now be accessible at `http://127.0.0.1:5050`.

## Running the Application

Once both the front-end and back-end servers are up and running, you can interact with the application by visiting the following URL:

- Front-end (React): `http://localhost:3000`
- Back-end (Flask API): `http://127.0.0.1:5050`

The front-end will handle user interactions, while the Flask API will process requests like restaurant searches, image-based cuisine detection, etc.

## Proxy Configuration

In the `package.json` file of the front-end, a proxy is configured to forward API requests to the Flask server running at `http://127.0.0.1:5050`. This ensures that front-end requests like `/api/restaurants` will be proxied to the back-end without needing to configure CORS.

To adjust the proxy, modify the following line in `package.json`:

```json
"proxy": "http://127.0.0.1:5050"
```
## API Endpoints

### 1. Restaurant by ID
- **URL**: `/restaurant_id/<int:restaurant_id>`
- **Method**: `GET`
- **Description**: Fetches details of a restaurant by its ID.
- **Response**:
    ```json
    {
        "id": 1,
        "name": "Example Restaurant",
        "cuisine": "Italian",
        "location": "Example Location",
        "avg_spend": "$$"
    }
    ```

### 2. Paginated Restaurant Search
- **URL**: \`/restaurants-paginated\`
- **Method**: \`GET\`
- **Description**: Searches for restaurants with pagination and optional filters such as cuisine, radius, and average spend.
- **Query Parameters**:
    - `cuisine`: Filter by cuisine type (optional).
    - `radius`: Search within a specific distance from the user (optional).
    - `avg_spend`: Filter by average spending (optional).
    - `page`: Page number for pagination.
- **Response**:
    ```json
    {
        "restaurants": [
            {
                "id": 1,
                "name": "Restaurant Name",
                "cuisine": "Cuisine Type",
                "location": "Location",
                "avg_spend": "$$",
                "distance": "2.5 km"
            },
            
        ],
        "pagination": {
            "page": 1,
            "total_pages": 5
        }
    }
    ```

### 3. Image-Based Restaurant Search
- **URL**: `/restaurants-by-image`
- **Method**: `POST`
- **Description**: Uploads an image of food and returns a list of restaurants that match the identified cuisine.
- **Request Payload**:
    ```json
    {
        "image": "<base64_encoded_image>"
    }
    ```
- **Response**:
    ```json
    {
        "restaurants": [
            {
                "id": 1,
                "name": "Restaurant Name",
                "cuisine": "Cuisine Type",
                "location": "Location",
                "avg_spend": "$$",
                "distance": "3.2 km"
            },
            
        ]
    }
    ```

---

## Proxy Configuration

The front-end (`React`) is configured to forward API requests to the Flask server (`http://127.0.0.1:5050`) via the `proxy` setting in `package.json`.

In the `front-end/package.json`, the following line exists:
```json
"proxy": "http://127.0.0.1:5050"
```
This ensures that API calls from the front-end are directed to the Flask back-end without needing additional CORS configuration.

---


## Outputs Explained

1. **Home Page - On Entry**:
   ![Home Page](https://github.com/user-attachments/assets/808da0c3-72e7-4d19-83a5-4df78923080a)

   

3. **Image Search on Basis of ID**:
   ![Image Search by ID](https://github.com/user-attachments/assets/15a26da7-a2ab-495f-b1a3-5a5ba652b318)

   

5. **Image Search and Pagination**:
   ![Image Search with Pagination](https://github.com/user-attachments/assets/d9752959-737f-4205-88f9-511086875031)

   

7. **Search on Basis of Cuisine and Cost**:
   ![Search by Cuisine and Cost](https://github.com/user-attachments/assets/611a20d8-07e4-431d-b075-c82db58990c2)




## License

This project is licensed under the MIT License.

