from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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
    if request.method == 'POST':
        data = request.get_json()
        new_dream = Dream(title=data['title'], description=data['description'], user_id=data['user_id'])
        db.session.add(new_dream)
        db.session.commit()
        return jsonify({'message': 'Dream added successfully'}), 201
    dreams = Dream.query.all()
    return jsonify([{'id': dream.id, 'title': dream.title, 'description': dream.description} for dream in dreams]), 200

@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        data = request.json
        new_user = User(username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'faulkner': 'User created successfully'}), 201
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users]), 200

if __name__ == '__main__':
    app.run(port=5000)