from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
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
def create_tables():
    db.create_all()

@app.route('/dreams', methods=['GET', 'POST'])
def manage_dreams():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'title' not in data or 'user_id' not in data:
                abort(400, description="Missing dream title or user_id")
            new_dream = Dream(title=data['title'], description=data.get('description', ''), user_id=data['user_id'])
            db.session.add(new_dream)
            db.session.commit()
            return jsonify({'message': 'Dream added successfully'}), 201
        dreams = Dream.query.all()
        return jsonify([{'id': dream.id, 'title': dream.title, 'description': dream.description} for dream in dreams]), 200
    except Exception as e:
        abort(500, description=str(e))

@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'username' not in data:
                abort(400, description="Missing username")
            new_user = User(username=data['username'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200
    except IntegrityError:
        abort(400, description="Duplicate username")
    except Exception as e:
        abort(500, description=str(e))

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error.description)}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(port=5000)