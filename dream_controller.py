from flask import Flask, request, jsonify
from dream_model import Dream  # Assuming dream_model is a module you've created for your Dream model
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()
database_uri = os.getenv("DATABASE_URI")

# Example function to connect to the database, modify as per your database setup
def connect_to_database():
    return None  # Add your database connection logic here

@app.route('/dreams', methods=['POST'])
def create_dream():
    # Connect to db
    db_connection = connect_to_database()
    dream_data = request.json
    # Assuming Dream model has a method to save to DB
    dream = Dream(title=dream_data.get('title'), description=dream_data.get('description'))
    # Add your logic to save 'dream' to the database
    return jsonify({'message': 'Dream created successfully', 'data': dream_data}), 201

@app.route('/dreams/<int:dream_id>', methods=['GET'])
def get_dream(dream_id):
    # Connect to db and get the dream by ID
    db_connection = connect_to_database()
    dream = None  # Replace with your logic to get a dream by ID from the database
    if dream:
        return jsonify({'data': dream})
    else:
        return jsonify({'message': 'Dream not found'}), 404

@app.route('/dreams/<int:dream_id>', methods=['PUT'])
def update_dream(dream_id):
    db_connection = connect_to_database()
    dream_data = request.json
    # Add your logic to find the dream by id and update it
    updated_dream = None  # Replace with your logic to update a dream in the database
    return jsonify({'message': 'Dream updated successfully', 'data': updated_dream}), 200

@app.route('/dreams/<int:dream_id>', methods=['DELETE'])
def delete_dream(dream_id):
    db_connection = connect_to_database()
    # Add your logic to find the dream by id and delete it
    # Respond with a success message
    return jsonify({'message': 'Dream deleted successfully'}), 204

@app.route('/dreams', methods=['GET'])
def list_dreams():
    # Connect to db and get all dreams
    db_connection = connect_to_database()
    dreams = []  # Replace with your logic to fetch all dreams from the database
    return jsonify({'data': dreams})

if __name__ == "__main__":
    app.run(debug=True)