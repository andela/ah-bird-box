from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class TestConfiguration(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = {
            "username": "gracie",
            "email": "graceunah@gmail.com",
            "password": "Unah12@$!"
        }

        self.user2 = {
            "username": "gracie2",
            "email": "graceunah2@gmail.com",
            "password": "Unah12@$!"
        }

        self.user_login = {
            "email": "graceunah@gmail.com",
            "password": "Unah12@$!"
        }

        self.user_login2 = {
            "email": "graceunah2@gmail.com",
            "password": "Unah12@$!"
        }

        self.article = {
            "title": "The fault in our stars",
            "body": "Really Awesome watch",
            "description": "A good starter movie",
            "author": "Caleb Rotich",
            "image_url": "https://demo.com"
        }

        self.stars = {
            "stars": 5
        }

        self.stars1 = {
            "stars": 50000000000
        }

        self.stars2 = {
            "stars": 500
        }

        self.register_url = reverse('authentication:register_user')
        self.login_url = reverse('authentication:login_user')
        self.create_article_url = reverse('articles:articles')
        self.wrong_slug = "the-fault-in-our-stars-wrong-2"

    def authenticate_user(self, data):
        """
        Create an active user in the database
        :return: user
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

    def create_article(self):
        """
        Create an article
        """
        self.authenticate_user(self.user)
        response = self.client.post(self.create_article_url,
                                    data=self.article,
                                    format='json')
        return response.data

    def get_ratings(self, slug):
        """
        Retrieve articles by users
        """
        url = reverse(
            'articles:rating:all_ratings', kwargs={"slug": slug})
        response = self.client.get(url)
        return response

    def rate(self, slug, stars=None):
        """
        Rate a an article by a user.
        """
        url = reverse(
            'articles:rating:all_ratings', kwargs={"slug": slug})
        response = self.client.post(url, data=stars, format='json')
        return response
