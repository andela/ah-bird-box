from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class TestConfiguration(APITestCase):
    """ Base class to suit all profile tests."""

    def setUp(self):
        """Initialize variables and methods used by the tests."""
        self.user = {
            "username": "gracie",
            "email": "graceunah@gmail.com",
            "password": "Unah12@$!"
        }

        self.user2 = {
            "username": "JohnDoe",
            "email": "johndoe@test.com",
            "password": "Test1@$!"
        }

        self.update_profile = {
            "bio": "Coder",
            "image": "https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/user.png",  # noqa
            "company": "Swatt",
            "website": "https://www.typepad.com/",
            "location": "Zambezi",
            "phone": "23655467"
        }

        self.user_login_details = {
            "user": {
                "email": "graceunah@gmail.com",
                "password": "Unah12@$!"

            }
        }
        self.wrong_user_login = {
            "user": {
                "email": "456g@gmail.com",
                "password": "Unah12@$!"
            }
        }

        self.client = APIClient()
        self.login_url = reverse('authentication:login_user')
        self.register_url = reverse('authentication:register_user')
        self.profiles_url = reverse('profile:authors_profile')

    def register_user(self, data):
        return self.client.post(
            self.register_url,
            data,
            format='json')

    def login_user(self, data):
        return self.client.post(
            self.user_login_details,
            data,
            format='json'
        )

    def edit_profile(self, username):
        url = self.profiles_url + '{}'.format(username)
        return self.client.put(
            url,
            self.user_bio, content_type="application/json")

    def authorize_user(self, user_login_details):
        # register a user
        self.register_user(data=self.user)
        payload = self.login_user(data=user_login_details)
        self.client.credentials(HTTP_AUTHORIZATION='token ' + payload['token'])
