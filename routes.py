from flask import Flask, Blueprint, request, jsonify
from flask_caching import Cache

from your_dream_controller import create_dream, get_dream, update_dream, delete_dream
from your_profile_controller import create_profile, get_profile, update_profile, delete_profile

app = Flask(__name__)

# Configuring cache, assuming simple in-memory caching for demonstration. 
# You can configure it for different backends as needed.
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 Minutes default cache timeout

cache = Cache(app)

dream_profile_bp = Blueprint('dream_profile_bp', __name__)

@app.route('/dream', methods=['POST'])
def add_dream():
    data = request.json
    try:
        response = create_dream(data)
        return response, 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/dream/<int:dream_id>', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # Caching for 1 minute
def retrieve_dream(dream_id):
    try:
        response = get_dream(dream_id)
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/dream/<int:dream_id>', methods=['PUT'])
def edit_dream(dream_id):
    data = request.json
    try:
        response = update_dream(dream_id, data)
        # Invalidate the cache for the updated resource
        cache.delete_memoized(retrieve_dream, dream_id)
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/dream/<int:dream_id>', methods=['DELETE'])
def remove_dream(dream_id):
    try:
        response = delete_dream(dream_id)
        # Invalidate the cache for the deleted resource
        cache.delete_memoized(retrieve_dream, dream_id)
        return response, 204
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/profile', methods=['POST'])
def add_profile():
    data = request.json
    try:
        response = create_profile(data)
        return response, 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/profile/<int:user_id>', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # Caching for 1 minute
def retrieve_profile(user_id):
    try:
        response = get_profile(user_id)
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/profile/<int:user_id>', methods=['PUT'])
def edit_profile(user_id):
    data = request.json
    try:
        response = update_profile(user_id, data)
        # Invalidate the cache for the updated resource
        cache.delete_memoized(retrieve_profile, user_id)
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/profile/<int:user_id>', methods=['DELETE'])
def remove_profile(user_id):
    try:
        response = delete_profile(user_id)
        # Invalidate the cache for the deleted resource
        cache.delete_memoized(retrieve_profile, user_id)
        return response, 204
    except Exception as e:
        return jsonify({'error': str(e)}), 404

# Register Blueprint
app.register_blueprint(dream_profile_bp)

if __name__ == '__main__':
    app.run(debug=True)