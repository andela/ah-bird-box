# Django imports
from rest_framework.views import status

# local imports
from .base_test import TestConfiguration


class TestSocialAuth(TestConfiguration):
    def base_400_test(self, data, error_key, message=None):
        """Base test for bad request"""
        response = self.client.post(
            self.social_auth_url, data, format='json')
        self.assertTrue(response.data[error_key])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        if message:
            self.assertIn(message.encode(), response.content)

    def base_200_test(self, data, key):
        response = self.client.post(
            self.social_auth_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[key])

    def test_successful_oauth2_login(self):
        """test successful oauth2 authentication with facebook"""

        self.base_200_test(self.oauth2_data, "username")

    def test_login_no_token(self):
        """test login with token not provided"""
        self.base_400_test(self.no_token_data, "errors")

    def test_login_with_invalid_token(self):
        """test login with a token that's invalid"""
        message = "Invalid token"
        self.base_400_test(self.invalid_token_data, "error", message)

    def test_login_no_provider(self):
        """test social login with provider name not provided"""
        self.base_400_test(self.no_provider_data, "errors")

    def test_invalid_provider(self):
        """test social login with invalid provider """
        message = "The Provider is invalid"
        self.base_400_test(self.invalid_provider_data, "error", message)
