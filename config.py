from datetime import timedelta

MONGOALCHEMY_DATABASE = 'logger'
MONGOALCHEMY_SERVER = 'mongodb'
MONGOALCHEMY_PORT = 27017
MONGOALCHEMY_SERVER_AUTH = False
SECRET_KEY = 'secret-O^#E#mo4ru'
JWT_EXPIRATION_DELTA = timedelta(seconds=3000000)
