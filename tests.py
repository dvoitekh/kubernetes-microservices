from app import app, db, jwt
from app.models import Application, Log

import unittest
import os
from flask import json

class AppTests(unittest.TestCase):
    # helpers
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        os.system("mongo logger --eval 'db.dropDatabase()'")

    def create_application(self, name, id, secret):
        return self.app.post('/applications',
            data=json.dumps(dict(name='test', id='id', secret='secret')),
            content_type='application/json')

    def login_headers(self, name, id, secret):
        self.create_application(name, id, secret)

        result = self.app.post('/auth',
            data=json.dumps(dict(username=id, password=secret)),
            content_type='application/json')

        return {'Authorization': 'JWT ' + json.loads(result.data)['access_token']}

    # test cases
    def test_valid_login(self):
        self.create_application('test', 'id', 'secret')

        result = self.app.post('/auth',
            data=json.dumps(dict(username='id', password='secret')),
            content_type='application/json')
        self.assertEqual(result.status_code, 200)

    def test_invalid_login(self):
        self.create_application('test', 'id', 'secret')

        result = self.app.post('/auth',
            data=json.dumps(dict(username='invalid_id', password='invalid_secret')),
            content_type='application/json')
        self.assertEqual(result.status_code, 401)

    def test_valid_applications_index(self):
        result = self.app.get('/applications')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'[]\n')

    def test_invalid_logs_index(self):
        result = self.app.get('/logs')
        self.assertEqual(result.status_code, 401)

    def test_valid_logs_index(self):
        result = self.app.get('/logs', headers=self.login_headers('test', 'id', 'secret'))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'[]\n')

if __name__ == '__main__':
    unittest.main()
