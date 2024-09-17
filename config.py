from flask import Flask
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

app = Flask(__name__)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///' + path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DEBUG'] = environ.get('DEBUG') == 'True'
app.config['FLASK_ENV'] = environ.get('FLASK_ENV') or 'development'