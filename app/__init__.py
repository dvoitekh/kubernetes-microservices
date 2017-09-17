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
from app.models import Application

def authenticate(username, password):
    print(username)
    print(password)
    print(Application.query.filter(Application.id == username and
        Application.secret == password).first().name)
    return Application.query.filter(Application.id == username and
        Application.secret == password).first()

def identity(payload):
    id = payload['identity']
    return Application.query.filter(Application.id == id).first()

jwt = JWT(app, authenticate, identity)
