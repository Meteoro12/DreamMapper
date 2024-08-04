from flask import Flask, request, jsonify
from dream_model import Dream  # Assuming dream_model is a module you've created for your Dream model
import os
from dotenv import load_dotenv
from functools import wraps

app = Flask(__name__)

# Load environment variables
load_dotenv()
database_uri = os.getenv("DATABASE_URI")

# Basic in-memory cache for demonstration purposes
cache = {
    'dreams': None
}

def validate_dream_input(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        dream_data = request.json
        if not dream_data or 'title' not in dream_data or 'description' not in dream_data:
            return jsonify({'message': 'Missing title or description'}), 400
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dreams', methods=['POST'])
@validate_dream_input
def create_dream():
    # Connect to db
    db_connection = connect_to_database()
    dream_data = request.json
    dream = Dream(title=dream_data['title'], description=dream_data['description'])
    # Logic to save 'dream' to the database
    # Invalidate or update cache as necessary
    cache['dreams'] = None  # Invalidate cache
    return jsonify({'message': 'Dream created successfully', 'data': dream_data}), 201

@app.route('/dreams/<int:dream_id>', methods=['GET'])
def get_dream(dream_id):
    db_connection = connect_to_database()
    dream = None  # Replace with logic to get a dream by ID from the database
    if dream:
        return jsonify({'data': dream})
    else:
        return jsonify({'message': 'Dream not found'}), 404

@app.route('/dreams', methods=['GET'])
def list_dreams():
    # Check if dreams are in cache first
    if cache['dreams'] is not None:
        return jsonify({'data': cache['dreams']})

    db_connection = connect_to_database()
    dreams = []  # Replace with logic to fetch all dreams from the database
    cache['dreams'] = dreams  # Store dreams in cache
    return jsonify({'data': dreams})

def connect_to_database():
    return None  # Your database connection logic here

if __name__ == "__main__":
    app.run(debug=True)