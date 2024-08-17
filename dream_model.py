from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, request, jsonify, abort
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

app = Flask(__name__)
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    dreams = db.relationship('Dream', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}')"


class Dream(db.Model):
    __tablename__ = 'dreams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f"Dream('{self.title}', '{self.date}')"


def initialize_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


@app.route('/dreams', methods=['POST'])
def add_dream():
    try:
        data = request.get_json(force=True)  # force=True to avoid errors if mimetype is not application/json
        title = data.get('title')
        content = data.get('content')
        user_id = data.get('user_id')
        if not title or not content or not user_id:
            return jsonify({'error': 'Missing title, content, or user ID'}), 400
        new_dream = Dream(title=title, content=content, user_id=user_id)
        db.session.add(new_dream)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except (TypeError, ValueError) as e:
        return jsonify({'error': 'Invalid input'}), 400
    return jsonify({'message': 'Dream created successfully'}), 201


@app.route('/dreams', methods=['GET'])
def get_dreams():
    try:
        dreams = Dream.query.all()
        output = []
        for dream in dreams:
            dream_data = {'title': dream.title, 'content': dream.content, 'user_id': dream.user_id}
            output.append(dream_data)
        return jsonify({'dreams': output})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/dreams/<int:id>', methods=['GET'])
def get_single_dream(id):
    try:
        dream = Dream.query.get_or_404(id)
        return jsonify({'title': dream.title, 'content': dream.content, 'user_id': dream.user_id})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/dreams/<int:id>', methods=['PUT'])
def update_dream(id):
    try:
        dream = Dream.query.get_or_404(id)
        data = request.get_json(force=True)
        dream.title = data.get('title', dream.title)  # Use existing value if not provided
        dream.content = data.get('content', dream.content)  # Use existing value if not provided
        db.session.commit()
        return jsonify({'message': 'Dream updated successfully'})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input'}), 400


@app.route('/dreams/<int:id>', methods=['DELETE'])
def delete_dream(id):
    try:
        dream = Dream.query.get_or_404(id)
        db.session.delete(dream)
        db.session.commit()
        return jsonify({'message': 'Dream deleted successfully'})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


initialize_db(app)

if __name__ == '__main__':
    app.run(debug=True)