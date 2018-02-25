import pymongo

from pymongo import Connection

from app import app


db = Connection(app.config['MONGO_HOST'],
                app.config['MONGO_PORT'])[app.config['MONGO_DB_NAME']]


class BaseRecord():
    COLLECTION = None

    def __init__(self, args):
        self.args = args

    def remove(self):
        self.__class__.remove(**self.args)

    @classmethod
    def create(cls, **kwargs):
        record = cls.COLLECTION.save(kwargs)
        return record and cls(kwargs)

    @classmethod
    def find_by(cls, **kwargs):
        record = cls.COLLECTION.find_one(kwargs)
        return record and cls(record)

    @classmethod
    def where(cls, **kwargs):
        records = cls.COLLECTION.find(kwargs)
        return [cls(record) for record in records]

    @classmethod
    def all(cls, **kwargs):
        records = cls.where()
        return [cls(record) for record in records]

    @classmethod
    def count(cls, **kwargs):
        return cls.COLLECTION.find(kwargs).count()

    @classmethod
    def remove(cls, **kwargs):
        cls.COLLECTION.remove(kwargs)


class Application(BaseRecord):
    COLLECTION = db.applications

    def __init__(self, args):
        super(Application, self).__init__(args)
        self._id = args['_id']
        self.user_id = args['user_id']
        self.secret = args['secret']
        self.name = args['name']
        self.created_at = args['created_at']


class Log(BaseRecord):
    COLLECTION = db.logs

    def __init__(self, args):
        super(Log, self).__init__(args)
        self._id = args['_id']
        self.application_id = args['application_id']
        self.request = args['request']
        self.ip_address = args['ip_address']
        self.created_at = args['created_at']

class User(BaseRecord):
    COLLECTION = db.users

    def __init__(self, args):
        super(User, self).__init__(args)
        self._id = args['_id']
        self.username = args['username']
        self.password = args['password']
        self.created_at = args['created_at']
