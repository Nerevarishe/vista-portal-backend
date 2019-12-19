from tests import FlaskBaseTestCase
from json import dumps


class NewsTestCase(FlaskBaseTestCase):

    def create_news_post(self, access_token):
        client = self.app.test_client()
        authorization = access_token
        # Post news post
        response = client.post('/news/', data=dumps({
            'postBody': 'Test message 1'
        }), headers={'Authorization': authorization}, content_type='application/json')
        if response.status_code == 201:
            return response.json['postId']

    def test_add_news_post(self):
        """ Try create new news post """

        client = self.app.test_client()
        authorization = self.create_user()
        # Post news post
        response = client.post('/news/', data=dumps({
            'postBody': 'I\'am test post'
        }), headers={'Authorization': authorization}, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_add_news_post_without_fields(self):
        """ Try create new news post without postBody field """

        client = self.app.test_client()
        authorization = self.create_user()
        # Post news post
        response = client.post('/news/', headers={'Authorization': authorization}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_news_post_with_blank_fields(self):
        """ Try create new news post with blank postBody field """

        client = self.app.test_client()
        authorization = self.create_user()
        # Post news post
        response = client.post('/news/', data=dumps({
            'postBody': ''
        }), headers={'Authorization': authorization}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_news_post(self):
        """ Try update new news post body"""

        client = self.app.test_client()
        authorization = self.create_user()
        news_post_id = self.create_news_post(authorization)
        response = client.put('/news/' + news_post_id,
                              data=dumps({'postBody': 'edited message 2'}), content_type='application/json',
                              headers={'Authorization': authorization})
        self.assertEqual(response.status_code, 200)

    def test_delete_news_post(self):
        """ Try delete new news post """

        client = self.app.test_client()
        authorization = self.create_user()
        news_post_id = self.create_news_post(authorization)
        response = client.delete('/news/' + news_post_id, content_type='application/json',
                                 headers={'Authorization': authorization})
        self.assertEqual(response.status_code, 200)

