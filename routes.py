from flask import Blueprint, request, jsonify

from your_dream_controller import create_dream, get_dream, update_dream, delete_dream
from your_profile_controller import create_profile, get_profile, update_profile, delete_profile

dream_profile_bp = Blueprint('dream_profile_bp', __name__)

@dream_profile_bp.route('/dream', methods=['POST'])
def add_dream():
    data = request.json
    try:
        response = create_dream(data)
        return response, 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@dream_profile_bp.route('/dream/<int:dream_id>', methods=['GET'])
def retrieve_dream(dream_id):
    try:
        response = get_dream(dream_id)
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@dream_profile_bp.route('/dream/<int:dream_id>', methods=['PUT'])
def edit_dream(dream_id):
    data = request.json
    try:
        response = update_dream(dream_id, data)
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@dream_profile_bp.route('/dream/<int:dream_id>', methods=['DELETE'])
def remove_dream(dream_id):
    try:
        response = delete_dream(dream_id)
        return response, 204
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@dream_profile_bp.route('/profile', methods=['POST'])
def add_profile():
    data = request.json
    try:
        response = create_profile(data)
        return response, 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@dream_profile_bp.route('/profile/<int:user_id>', methods=['GET'])
def retrieve_profile(user_id):
    try:
        response = get_profile(user_id)
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@dream_profile_bp.route('/profile/<int:user_id>', methods=['PUT'])
def edit_profile(user_id):
    data = request.json
    try:
        response = update_profile(user_id, data)
        return response, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@dream_profile_bp.route('/profile/<int:user_id>', methods=['DELETE'])
def remove_profile(user_id):
    try:
        response = delete_profile(user_id)
        return response, 204
    except Exception as e:
        return jsonify({'error': str(e)}), 404