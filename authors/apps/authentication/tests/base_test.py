from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestConfiguration(APITestCase):
    """ Base class to suit all authentication tests."""

    def setUp(self):
        """Initialize variables and methods used by the tests."""
        self.user = {
            "user": {
                "username": "gracie",
                "email": "graceunah@gmail.com",
                "password": "Unah12@$!"
            }
        }

        self.client = APIClient()
        self.login_url = reverse('authentication:login_user')
        self.register_url = reverse('authentication:register_user')

        self.empty_payload = {
            "user": {}
        }

        self.user_wrong_email_format = {
            "user": {
                "username": "sammy",
                "email": "samsamsam",
                "password": "sam232#$$"
            }
        }

        self.username = {
            "user": {
                "username": "Jacob",
                "email": "lolisme2016@gmail.com",
                "password": "manu232#$$"
            }
        }

        self.username1 = {
            "user": {
                "username": "Jacob",
                "email": "jake1@jake.jake",
                "password": "manu232#$$"
            }
        }
        self.user_empty_email = {
            "user": {
                "username": "Rakel",
                "email": "",
                "password": "noni232#$$"
            }
        }
        self.user_empty_username = {
            "user": {
                "username": "",
                "email": "jake@jake.com",
                "password": "manu232#$$"
            }
        }
        self.user_empty_password = {
            "user": {
                "username": "jake",
                "email": "jake@jake.com",
                "password": ""
            }
        }

        self.user_short_password = {
            'user': {
                'username': 'nimo',
                'email': 'nimo@gmail.com',
                'password': 'me1'
            }
        }

        self.user_login = {
            "user": {
                "email": "graceunah@gmail.com",
                "password": "Unah12@$!"
            }
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
