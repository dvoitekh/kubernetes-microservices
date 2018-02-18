from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_jwt import JWT

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
# Load the config file
app.config.from_object('config')
# Initialize db
db = MongoAlchemy(app)

from app import views
from app.models import User


def authenticate(username, password):
    return User.query.filter(User.username == username and
                             User.password == password).first()


def identity(payload):
    id = payload['identity']
    return User.query.filter(User.id == id).first()


jwt = JWT(app, authenticate, identity)
