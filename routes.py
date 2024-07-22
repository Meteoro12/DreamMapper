from flask import Blueprint, request, jsonify
from your_dream_controller import create_dream, get_dream, update_dream, delete_dream
from your_profile_controller import create_profile, get_profile, update_profile, delete_profile

dream_profile_bp = Blueprint('dream_profile_bp', __name__)

@dream_profile_bp.route('/dream', methods=['POST'])
def add_dream():
    data = request.json
    return create_dream(data)

@dream_profile_bp.route('/dream/<int:dream_id>', methods=['GET'])
def retrieve_dream(dream_id):
    return get_dream(dream_id)

@dream_profile_bp.route('/dream/<int:dream_id>', methods=['PUT'])
def edit_dream(dream_id):
    data = request.json
    return update_dream(dream_id, data)

@dream_profile_bp.route('/dream/<int:dream_id>', methods=['DELETE'])
def remove_dream(dream_id):
    return delete_dream(dream_id)

@dream_profile_bp.route('/profile', methods=['POST'])
def add_profile():
    data = request.json
    return create_profile(data)

@dream_profile_bp.route('/profile/<int:user_id>', methods=['GET'])
def retrieve_profile(user_id):
    return get_profile(user_id)

@dream_profile_bp.route('/profile/<int:user_id>', methods=['PUT'])
def edit_profile(user_id):
    data = request.json
    return update_profile(user_id, data)

@dream_profile_bp.route('/profile/<int:user_id>', methods=['DELETE'])
def remove_profile(user_id):
    return delete_profile(user_id)