from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from authors.apps.authentication.models import User


class TestConfiguration(APITestCase):
    def setUp(self):
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

        self.reader = self.create_user(self.user)
        self.author = self.create_user(self.user2)
        self.slug = self.create_article().data['slug']
        self.slug2 = "the-fault-in-our-stars-wrong-2"
        self.client = APIClient()
        self.one_article_url = reverse("articles:article-details",
                                       kwargs={"slug": self.slug})
        self.ratings_url = reverse('articles:rating:all_ratings', kwargs={
            "slug": self.slug})
        self.ratings_url2 = reverse('articles:rating:all_ratings', kwargs={
            "slug": self.slug2})

    def create_user(self, user):
        """
        Create an active user in the database
        :return: user
        """
        user = User.objects.create_user(
            email=user['email'],
            username=user['username'],
            password=user['password'],
        )
        user.is_active = True
        user.save()
        return user

    def user_login_req(self, data):
        self.login_url = reverse('authentication:login_user')
        return self.client.post(
            self.login_url,
            data=data,
            format="json")

    def login(self, data):
        response = self.user_login_req(data=data)
        return response.data['token']

    def create_article(self):
        """
        Create an article
        """
        create_article_url = reverse('articles:articles')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.login(data=self.user_login2))
        response = self.client.post(create_article_url,
                                    data=self.article,
                                    format='json')
        return response

    def get_ratings(self, user=None, is_authenticated=False,
                    is_found=True, url=None):
        """
        Retrieve articles by users
        """

        if user:
            login = self.user_login2
        else:
            login = self.user_login

        if is_authenticated:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer ' +
                self.login(data=login)
            )
            response = self.client.get(url)
            return response
        else:
            response = self.client.get(url)
            return response

    def rate(self, user=None, is_authenticated=True, is_found=True,
             stars=None, url=None):
        """
        Rate a an article by a user.
        """
        if user:
            login = self.user_login2
        else:
            login = self.user_login

        if is_authenticated:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer ' +
                self.login(data=login)
            )
            response = self.client.post(url,
                                        data=stars,
                                        format='json')
            return response
        else:
            response = self.client.post(url,
                                        data=stars,
                                        format='json')
            return response
