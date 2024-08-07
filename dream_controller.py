from flask import Flask, request, jsonify
from dream_model import Dream
import os
from dotenv import load_dotenv
from functools import wraps
import sqlite3

app = Flask(__name__)

load_dotenv()
database_uri = os.getenv("DATABASE_URI")

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

def handle_db_connection_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return jsonify({'message': 'Database error, please try again later.'}), 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({'message': 'Unexpected error occurred, please try again later.'}), 500
    return decorated_function

@app.route('/dreams', methods=['POST'])
@validate_dream_input
@handle_db_connection_errors
def create_dream():
    db_connection = connect_to_database()
    dream_data = request.json
    dream = Dream(title=dream_data['title'], description=dream_data['description'])
    cache['dreams'] = None
    return jsonify({'message': 'Dream created successfully', 'data': dream_data}), 201

@app.route('/dreams/<int:dream_id>', methods=['GET'])
@handle_db_connection_errors
def get_dream(dream_id):
    db_connection = connect_to_database()
    dream = None
    if dream:
        return jsonify({'data': dream})
    else:
        return jsonify({'message': 'Dream not found'}), 404

@app.route('/dreams', methods=['GET'])
@handle_db_connection_errors
def list_dreams():
    if cache['dreams'] is not None:
        return jsonify({'data': cache['dreams']})

    db_connection = connect_to_database()
    dreams = []
    cache['dreams'] = dreams
    return jsonify({'data': dreams})

def connect_to_database():
    try:
        conn = sqlite3.connect(database_uri)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise

if __name__ == "__main__":
    app.run(debug=True)