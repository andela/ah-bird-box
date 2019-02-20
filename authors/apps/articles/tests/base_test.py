from django.urls import reverse
from rest_framework.test import APITestCase


class TestBaseCase(APITestCase):
    def setUp(self):
        self.signup_url = reverse('authentication:register_user')
        self.login_url = reverse('authentication:login_user')
        self.create_list_article_url = reverse('articles:articles')
        self.wrong_slug = "the-fault-in-our-stars-wrong-2"
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

    def verify_user_registration(self, token):
        verify_url = reverse('authentication:verify_email', args=[token])
        self.client.get(verify_url)

    def authenticate_user(self, data):
        """
        Create an active user in the database
        :return: user
        """

        response = self.client.post(
            self.signup_url, data, format='json')
        token = response.data['user_info']['token']
        self.verify_user_registration(token)
        response = self.client.post(
            self.login_url, data, format='json'
        )
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def create_article(self):
        response = self.client.post(
            self.create_list_article_url, self.article, format='json')
        return response

    def single_article_url(self, slug):
        return reverse('articles:article-details', args=[slug])

    def like_article(self, slug):
        return self.client.put(
            reverse('articles:likes', kwargs={"slug": slug}),
            format='json')

    def dislike_article(self, slug):
        return self.client.put(
            reverse('articles:dislikes', kwargs={"slug": slug}),
            format='json')
