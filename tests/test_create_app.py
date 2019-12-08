from tests import FlaskBaseTestCase


class AppStartTestCase(FlaskBaseTestCase):
    def setUp(self) -> None:
        super(AppStartTestCase, self).setUp()
        @self.app.route('/', methods=['GET'])
        def index():
            return "TEST"

    def test_index(self):
        client = self.app.test_client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)