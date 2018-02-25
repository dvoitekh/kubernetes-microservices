from flask import jsonify
from app.models import Application, Log, User

class BaseSerializer(object):
    FIELDS = []

    def __init__(self, records, extra_fields=[]):
        self._records = records
        self._extra_fields = extra_fields

    def _get_object_property(self, object, property):
        try:
            return getattr(object, property)
        except Exception as e:
            return None

    def _mongo_object_to_dic(self, object):
        return {field: self._get_object_property(object, field) for field in self.FIELDS + self._extra_fields}

    def serialize(self):
        result = None
        if isinstance(self._records, list):
            result = [self._mongo_object_to_dic(record) for record in self._records]
        else:
            result = self._mongo_object_to_dic(self._records)
        return jsonify(result)


class ApplicationSerializer(BaseSerializer):
    FIELDS = ['_id', 'name', 'user_id', 'created_at']


class LogSerializer(BaseSerializer):
    FIELDS = ['_id', 'application_id', 'request', 'ip_address', 'created_at']


class UserSerializer(BaseSerializer):
    FIELDS = ['_id', 'username', 'password', 'created_at']
