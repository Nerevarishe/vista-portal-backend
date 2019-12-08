import unittest
from config import TestConfig
from app import create_app
import mongoengine
from mongoengine import connect


class FlaskBaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(config_class=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        # mongoengine.connection._connection_settings.clear()
        # mongoengine.connection._connections.clear()
        # mongoengine.connection._dbs.clear()

    def tearDown(self) -> None:
        self.app_context.pop()
        db = connect(self.app.config['MONGODB_DB'], host=self.app.config['MONGODB_HOST'])
        db.drop_database(self.app.config['MONGODB_DB'])
