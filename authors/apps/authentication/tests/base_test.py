import os
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestConfiguration(APITestCase):
    """ Base class to suit all authentication tests."""

    def setUp(self):
        """Initialize variables and methods used by the tests."""
        self.user = {
                "username": "gracie",
                "email": "graceunah@gmail.com",
                "password": "Unah12@$!"
        }

        self.social_auth_url = reverse('authentication:social_auth')
        self.invalid_token = 'this.is.an.invalid.token.for.social.login.test.purpose' # noqa
        self.oauth2_token = os.getenv("OAUTH2_ACCESS_TOKEN")

        self.invalid_provider_data = {
            "provider": "invalidprovider",
            "access_token": self.oauth2_token
        }

        self.invalid_token_data = {
            "provider": "facebook",
            "access_token": self.invalid_token
        }

        self.oauth2_data = {
            "provider": "facebook",
            "access_token": self.oauth2_token
        }

        self.no_token_data = {
            "provider": "facebook"
        }

        self.no_provider_data = {
            "access_token": self.oauth2_token
        }

        self.client = APIClient()
        self.login_url = reverse('authentication:login_user')
        self.register_url = reverse('authentication:register_user')

        self.empty_payload = {}

        self.user_wrong_email_format = {
                "username": "sammy",
                "email": "samsamsam",
                "password": "sam232#$$"
        }

        self.username = {
                "username": "Jacob",
                "email": "lolisme2016@gmail.com",
                "password": "manu232#$$"
        }

        self.username1 = {
                "username": "Jacob",
                "email": "jake1@jake.jake",
                "password": "manu232#$$"
        }
        self.user_empty_email = {
                "username": "Rakel",
                "email": "",
                "password": "noni232#$$"
        }
        self.user_empty_username = {
                "username": "",
                "email": "jake@jake.com",
                "password": "manu232#$$"
        }
        self.user_empty_password = {
                "username": "jake",
                "email": "jake@jake.com",
                "password": ""
        }

        self.user_short_password = {
                'username': 'nimo',
                'email': 'nimo@gmail.com',
                'password': 'me1'
        }

        self.user_login = {
                "email": "graceunah@gmail.com",
                "password": "Unah12@$!"
        }

        self.invalid_username = {
                'username': '666778',
                'email': 'gracie@gmail.com',
                'password': 'me1hn5u*%h5'
        }

        self.user_non_alphanumeric_password = {
                'username': 'claudia',
                'email': 'claudia@gmail.com',
                'password': 'passnjsnffsfn'
        }

    def register_user(self, data):
        return self.client.post(
            self.register_url,
            data,
            format='json'
        )

    def user_login_req(self, data):
        return self.client.post(
            self.login_url,
            data=data,
            format="json")
