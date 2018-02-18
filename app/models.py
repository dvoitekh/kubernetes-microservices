from app import db
from mongoalchemy.document import Index


class Application(db.Document):
    id = db.StringField()
    user_id = db.IntField()
    secret = db.StringField()
    name = db.StringField()
    created_at = db.DateTimeField()

    id_index = Index().ascending('id').unique()
    secret_index = Index().ascending('secret').unique()


class Log(db.Document):
    application_id = db.StringField()
    request = db.DictField(db.StringField())
    ip_address = db.StringField()
    created_at = db.DateTimeField()


class User(db.Document):
    id = db.IntField()
    username = db.StringField()
    password = db.StringField()
    created_at = db.DateTimeField()
