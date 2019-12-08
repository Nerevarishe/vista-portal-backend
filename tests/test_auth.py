from tests import FlaskBaseTestCase
from json import dumps
from flask import jsonify
from flask_mongoengine import MongoEngine
from flask_jwt_extended import jwt_required
from app.models import User


class AuthTestCase(FlaskBaseTestCase):
    def setUp(self) -> None:
        super(AuthTestCase, self).setUp()
        db = MongoEngine()
        db.init_app(self.app)
        User.drop_collection()
        self.User = User

    def test_register_user(self):
        """ Try register user """

        client = self.app.test_client()
        response = client.post('/auth/register',
                               data=dumps({
                                   'username': 'Test1',
                                   'password': 'test1'
                               }),
                               content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_register_user_no_fields(self):
        """ Try register user with no json fields in request """

        client = self.app.test_client()
        response = client.post('/auth/register')
        self.assertEqual(response.status_code, 400)

    def test_register_user_no_user_field(self):
        """ Try register user with no username field in request """

        client = self.app.test_client()
        response = client.post('/auth/register',
                               data=dumps({
                                   'password': 'test1'
                               }),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_no_password_field(self):
        """ Try register user with no password field """

        client = self.app.test_client()
        response = client.post('/auth/register',
                               data=dumps({
                                   'username': 'Test1'
                               }),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_with_same_username(self):
        """ Try register user with same username """

        client = self.app.test_client()
        response = client.post('/auth/register',
                               data=dumps({
                                   'username': 'Test1',
                                   'password': 'test1'
                               }),
                               content_type='application/json')
        if response.status_code == 201:
            response = client.post('/auth/register',
                                   data=dumps({
                                       'username': 'Test1',
                                       'password': 'test1'
                                   }),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 409)

    def test_normal_user_login(self):
        """ Try login user """

        # First register User
        client = self.app.test_client()
        response = client.post('/auth/register',
                               data=dumps({
                                   'username': 'Test1',
                                   'password': 'test1'
                               }),
                               content_type='application/json')

        # If register successful:
        if response.status_code == 201:
            response = client.post('/auth/login',
                                   data=dumps({
                                    'username': 'Test1',
                                    'password': 'test1'
                                   }),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 200)

    def test_login_user_without_fields(self):
        """ Try login user """

        # First register User
        client = self.app.test_client()
        response = client.post('/auth/register',
                               data=dumps({
                                   'username': 'Test1',
                                   'password': 'test1'
                               }),
                               content_type='application/json')

        # If register successful:
        if response.status_code == 201:
            response = client.post('/auth/login')
            self.assertEqual(response.status_code, 400)

    def test_login_user_without_username_field(self):
        """ Try login user """

        # First register User
        client = self.app.test_client()
        response = client.post('/auth/register',
                               data=dumps({
                                   'username': 'Test1',
                                   'password': 'test1'
                               }),
                               content_type='application/json')

        # If register successful:
        if response.status_code == 201:
            response = client.post('/auth/register',
                                   data=dumps({
                                       'password': 'test1'
                                   }),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_login_user_without_password_field(self):
        """ Try login user """

        # First register User
        client = self.app.test_client()
        response = client.post('/auth/register',
                               data=dumps({
                                   'username': 'Test1',
                                   'password': 'test1'
                               }),
                               content_type='application/json')

        # If register successful:
        if response.status_code == 201:
            response = client.post('/auth/register',
                                   data=dumps({
                                       'username': 'Test1'
                                   }),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 400)


class AuthAccessCase(FlaskBaseTestCase):
    def setUp(self) -> None:
        super(AuthAccessCase, self).setUp()
        db = MongoEngine()
        db.init_app(self.app)
        User.drop_collection()
        self.User = User
        @self.app.route('/test', methods=['GET'])
        @jwt_required
        def test_route():
            return jsonify({
                'msg': 'ok',
                'destination': 'test auth route'
            }), 200

    def test_access_to_jwt_required_route(self):
        """ Try login user """

        # First register User
        client = self.app.test_client()
        response = client.post('/auth/register',
                               data=dumps({
                                   'username': 'Test1',
                                   'password': 'test1'
                               }),
                               content_type='application/json')

        # If register successful try login:
        if response.status_code == 201:
            response = client.post('/auth/login',
                                   data=dumps({
                                       'username': 'Test1',
                                       'password': 'test1'
                                   }),
                                   content_type='application/json')
            # If login successful, try go to private route
            if response.status_code == 200:
                access_token = response.json['access_token']
                authorization = 'Bearer ' + access_token
                response = client.get('/test', headers={'Authorization': authorization})
                self.assertEqual(response.status_code, 200)
