from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityTimeoutError
from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database configuration
DATABASE_URI = getenv('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Dream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('dreams', lazy=True))

@app.before_first_request
def initialize_database():
    """Create database tables if they don't already exist."""
    db.create_all()

@app.route('/dreams', methods=['GET', 'POST'])
def handle_dreams():
    """Retrieve all dreams or add a new dream."""
    try:
        if request.method == 'POST':
            dream_data = request.get_json()
            if not dream_data or 'title' not in dream_data or 'user_id' not in dream_data:
                abort(400, description="Missing dream title or user_id")
            new_dream = Dream(title=dream_data['title'], description=dream_data.get('description', ''), user_id=dream_data['user_id'])
            db.session.add(new_dream)
            db.session.commit()
            return jsonify({'message': 'Dream added successfully'}), 201
        
        dreams_query = Dream.query.all()
        dreams_list = [{'id': dream.id, 'title': dream.title, 'description': dream.description} for dream in dreams_query]
        return jsonify(dreams_list), 200
    except Exception as error:
        abort(500, description=str(error))

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    """Retrieve all users or add a new user."""
    try:
        if request.method == 'POST':
            user_data = request.get_json()
            if not user_data or 'username' not in user_data:
                abort(400, description="Missing username")
            new_user = User(username=user_data['username'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        
        users_query = User.query.all()
        users_list = [{'id': user.id, 'username': user.username} for user in users_initiative]
        return jsonify(users_list), 200
    except IntegrityTimeoutError:
        abort(400, description="Duplicate username")
    except Exception as error:
        abort(500, description=str(error))

@app.errorhandler(404)
def handle_not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def handle_bad_request(error):
    """Handle 400 errors."""
    return jsonify({'error': str(error.description)}), 400

@app.errorhandler(500)
def handle_internal_error(error):
    """Handle 500 internal server errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(port=5000)