from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.utils.text import slugify


class BaseTest(APITestCase):
    """
    Base Test functions to allow for code reuse
    """

    def setUp(self):
        """
        Methos to run automatically when tests are executed
        """
        self.client = APIClient()
        self.register_url = reverse('authentication:register_user')
        self.login_url = reverse('authentication:login_user')
        self.articles_url = reverse('articles:articles')

        self.sample_user = {
            "username": "ahbirdbox03",
            "email": "ahbirdbox03@gmail.com",
            "password": "Birdbox@2019"
        }
        self.sample_wrong_user_details = {
            "username": "ahbirdbox",
            "email": "ahbirdbox@gmail.com",
            "password": "birdbox@2019"
        }

        self.sample_comment = {
                "body": "I am a comment"
        }

        self.sample_updated_comment = {
                "body": "I was a comment"
        }

        self.sample_null_comment_body = {
                "body": ""
        }

        self.sample_article = {
                "title": "My Data",
                "description": "This is my data",
                "body": "This article was written by me",
                "tagList": ['test'],
                "author": 1
        }

    def comment_url(self, slug):
        """
        Generate the comment url
        """
        url = "/api/articles/{}/comments/".format(slug)
        return url

    def create_article(self, article):
        """
        Create a dummy to be used in the tests
        """
        self.client.post(self.articles_url, article, format='json')

    def create_comment(self, comment_data, article):
        """
        An abstract method to create a comment
        """
        return self.client.post(
            self.comment_url(slugify(article['title'])),
            comment_data,
            format='json'
        )

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

    def verify_user_registration(self, token):
        verify_url = reverse('authentication:verify_email', args=[token])
        self.client.get(verify_url)
