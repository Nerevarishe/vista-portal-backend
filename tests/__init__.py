import unittest
from config import TestConfig
from app import create_app
from flask_mongoengine import MongoEngine
from mongoengine import connect
from json import dumps


class FlaskBaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(config_class=TestConfig)
        self.app_context = self.app.app_context()
        db = MongoEngine()
        db.init_app(self.app)
        self.app_context.push()

    def tearDown(self) -> None:
        self.app_context.pop()
        db = connect(self.app.config['MONGODB_DB'], host=self.app.config['MONGODB_HOST'])
        db.drop_database(self.app.config['MONGODB_DB'])

    def create_user(self):
        client = self.app.test_client()
        # Create new User
        response = client.post('/auth/register', data=dumps({
            'username': 'admin',
            'password': 'admin'
        }), content_type='application/json')
        if response.status_code == 201:
            access_token = response.json['access_token']
            authorization = 'Bearer ' + access_token
            return authorization
        return False
