from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class BaseTestCase(TestCase):
    """
    Base tests to be used by all other tests
    """
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('authentication:register_user')
        self.login_url = reverse('authentication:login_user')
        self.articles_url = reverse('articles:articles')
        self.create_list_article_url = reverse('articles:articles')
        self.subscribe_url = reverse('notifications:subscribe')

        self.subscribe_data = {
            "email": True,
            "app": True
            }

        self.article_author = {
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "this_user123@A"
        }

        self.author_data = {
            "email": "testuser@gmail.com",
            "password": "this_user123@A"
        }
        self.article = {
                "title": "Test Article",
                "description": "Test description for the article",
                "body": "Test body for the article",
                "author": 1
        }
        self.article_details = {
            "title": "your first blog",
            "description": "this is your first blog",
            "body": "this is your first blog",
            "tagList": ["dragons", "training"],
        }

        self.follower = {
            "username": "rainy",
            "email": "greisunah@gmail.com",
            "password": "this_user123@A"
        }

        self.follower_data = {"user": {
            "email": "greisunah@gmail.com",
            "password": "this_user123@A"
        }}

        self.follower2 = {
            "username": "maggy66",
            "email": "maggy@gmail.com",
            "password": "this_user123@A"
        }

        self.follower2_data = {
            "email": "maggy@gmail.com",
            "password": "this_user123@A"
        }

    def authenticate_user(self, data):
        """
        Register and login an authorized user
        """
        response = self.client.post(
            self.register_url, data, format='json')
        token = response.data['user_info']['token']
        self.verify_user_registration(token)
        response = self.client.post(
            self.login_url, data, format='json'
        )
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return token

    def verify_user_registration(self, token):
        verify_url = reverse('authentication:verify_email', args=[token])
        self.client.get(verify_url)

    def create_article(self):
        response = self.client.post(
            self.create_list_article_url, self.article, format='json')
        return response
