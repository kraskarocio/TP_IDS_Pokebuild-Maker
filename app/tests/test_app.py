from app import app

import unittest

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_user(self):
        response = self.app.post('/api/add_user/', json={
            'username': 'test',
            'password': 'test',
            'email': 'esto@esun.test'
        })
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'User added successfully'})


if __name__ == '__main__':
    unittest.main()
