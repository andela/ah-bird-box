import os
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.core import mail
from bs4 import BeautifulSoup
import re
from authors.apps.authentication.models import User


class TestConfiguration(APITestCase):
    """ Base class to suit all authentication tests."""

    def setUp(self):
        """Initialize variables and methods used by the tests."""
        self.user = {
            "username": "gracie",
            "email": "graceunah@gmail.com",
            "password": "Unah12@$!"
        }

        self.user_update = {
            "username": "gracie44",
            "email": "graceunah.44@gmail.com",
            "password": "Unah12@$!"
        }

        self.user2 = {
            "username": "JohnDoe",
            "email": "johndoe@test.com",
            "password": "Test1@$!"
        }

        self.update_profile = {
            "bio": "Writer",
            "company": "Andela",
            "website": "https://www.andela.com",
            "location": "Nairobi",
            "phone": "+2547123456"
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
            "provider": "google-oauth2",
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
        self.specific_user_url = reverse('authentication:specific_user')
        self.user_profile_url = reverse('profile:profile',
                                        kwargs={'username': 'gracie'})
        self.all_profiles_url = reverse('profile:authors_profile')
        self.invalid_token = 'thsnmbnscjkxcmm.btydghvhjb'
        self.invalid_token2 = 't'
        self.password_reset_url = reverse('authentication:reset_password')

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
        self.passwords = {
            'password': '@Birdbox2019',
            'confirm_password': '@Birdbox2019'
        }
        self.unmatched_passwords = {
            'password': '@Birdbox2019',
            'confirm_password': '@Birdbox2018'
        }

        self.resend_url = {
            'email': 'graceunah@gmail.com'

        }

        self.resend_blank_email = {
            'email': ''
        }

        self.resend_wrong_email_format = {
            'email': 'memeemnjd.com'
        }

    def register_user(self, data):
        return self.client.post(
            self.register_url,
            data,
            format='json')

    def user_login_req(self, data):
        return self.client.post(
            self.login_url,
            data=data,
            format="json")

    def get_user(self):
        return self.client.get(
            self.specific_user_url,
            format="json")

    def update_user(self, data):
        return self.client.put(
            self.specific_user_url,
            data=data,
            format="json")

    def get_user_token(self):
        self.register_user(data=self.user)
        user = User.objects.get(email=self.user['email'])
        user.is_verified = True
        user.save()
        response = self.user_login_req(data=self.user_login)
        return response.data['token']

    def get_token_from_email(self):
        self.register_user(data=self.user)
        mail.outbox = []
        self.client.post(
            self.password_reset_url, data={"email": "graceunah@gmail.com"},
            format='json'
        )
        email = mail.outbox[0].alternatives[0][0]
        soup = BeautifulSoup(email, 'html.parser')
        link = soup.a['href']
        token = re.search(r'(?<=update_password/)(.*)', link).group(1)
        return token

    def follow_user(self, username, token):
        """This method sends a follow request to a user"""
        follow_url = reverse("profile:follow", kwargs={'username': username})
        response = self.client.post(
            follow_url,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        return response

    def unfollow_user(self, username, token):
        """This method sends a follow request to a user"""
        follow_url = reverse("profile:follow", kwargs={'username': username})
        response = self.client.delete(
            follow_url,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        return response

    def get_following(self, username, token):
        """This method sends a follow request to a user"""
        following_url = reverse("profile:following",
                                kwargs={'username': username})
        response = self.client.get(
            following_url,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        return response

    def edit_profile_url(self, username):
        return reverse('profile:update_profile',
                       kwargs={'username': username})
