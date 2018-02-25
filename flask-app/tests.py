from app import app, db, jwt

import unittest
import os

class AppTests(unittest.TestCase):
    # helpers
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        os.system("mongo logger --eval 'db.dropDatabase()'")

    # test cases
    def test_valid_applications_index(self):
        result = self.app.get('/applications')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'[]\n')

    def test_invalid_logs_index(self):
        result = self.app.get('/logs')
        self.assertEqual(result.status_code, 401)

if __name__ == '__main__':
    unittest.main()
