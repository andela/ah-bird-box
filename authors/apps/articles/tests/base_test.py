from django.urls import reverse
from rest_framework.test import APITestCase


class TestBaseCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('authentication:register_user')
        self.login_url = reverse('authentication:login_user')
        self.create_list_article_url = reverse('articles:articles')
        self.test_user = {
                'username': 'Test',
                'email': 'test@user.com',
                'password': 'Password12#'
            }
        self.article = {
                "title": "Test Article",
                "description": "Test description for the article",
                "body": "Test body for the article",
                "author": 1
        }
        self.updated_article = {
                "title": "Updated Title",
                "body": "Updated body"
        }

    def signup_user(self):
        return self.client.post(self.signup_url,
                                self.test_user,
                                format='json')

    def login_user(self):
        self.signup_user()
        response = self.client.post(self.login_url,
                                    self.test_user,
                                    format='json')

        return response.data['token']

    def create_article(self):
        response = self.client.post(
            self.create_list_article_url, self.article, format='json',
            HTTP_AUTHORIZATION="Bearer " + self.login_user())
        return response.data['slug']

    def single_article_url(self, slug):
        return reverse('articles:article-details', args=[slug])
