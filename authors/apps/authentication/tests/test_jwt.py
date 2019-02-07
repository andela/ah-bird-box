from rest_framework.views import status
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base_test import TestConfiguration


class JwtTestCase(TestConfiguration):
    """JWT configuration and generation test case"""

    def test_token_generation_with_user_registration(self):
        """Test token generation at signup."""

        response = self.register_user(data=self.user2)
        self.assertEqual(response.data['email'], "johndoe@test.com")
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_generation_with_user_login(self):
        """Test token generation at login."""

        self.register_user(data=self.user)
        response = self.user_login_req(data=self.user_login)
        self.assertEqual(response.data['email'], "graceunah@gmail.com")
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        """Test to get user with token in the request"""

        self.token = self.get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.get_user()
        self.assertEqual(response.data['email'], "graceunah@gmail.com")
        self.assertEqual(response.status_code, 200)

    def test_get_user_no_token(self):
        """Test getting a user with no token in the request"""

        response = self.get_user()
        self.assertEqual(response.status_code, 403)
        msg = "Authentication credentials were not provided."
        self.assertEqual(response.data["detail"], msg)

    def test_get_user_invalid_token(self):
        """Test getting a user with an expired or invalid token"""

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.invalid_token)
        response = self.get_user()
        self.assertEqual(response.status_code, 403)
        msg = "Invalid token. Token decode failed"
        self.assertEqual(response.data["detail"], msg)

    def test_get_user_short_token(self):
        """Test getting a user with an invalid length token"""

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.invalid_token2)
        response = self.get_user()
        self.assertEqual(response.status_code, 403)
        msg = "Invalid token. Token decode failed"
        self.assertEqual(response.data["detail"], msg)

    def test_get_non_existent_user(self):
        """Test getting a user who doesn't exist"""

        self.token = self.get_user_token()
        self.email = self.user['email']
        User.objects.get(email=self.email).delete()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.get_user()
        self.assertEqual(response.status_code, 403)
        msg = "No user matching this token"
        self.assertEqual(response.data["detail"], msg)

    def test_get_user_no_bearer(self):
        """Test getting a user without prefix authorisation  in the header"""

        self.token = self.get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.get_user()
        self.assertEqual(response.status_code, 403)
        msg = "Invalid authorization header"
        self.assertEqual(response.data["detail"], msg)

    def test_get_user_wrong_prefix(self):
        """Test getting a user with wrong prefix authorisation in the header"""

        self.token = self.get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION='Test ' + self.token)
        response = self.update_user(self.user_update)
        self.assertEqual(response.status_code, 403)
        msg = "Use a Bearer Token"
        self.assertEqual(response.data["detail"], msg)

    def test_update_user(self):
        """Test to update user with token in the request"""

        self.token = self.get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.update_user(self.user_update)
        self.assertEqual(response.data['email'], "graceunah.44@gmail.com")
        self.assertEqual(response.status_code, 200)

    def test_update_user_no_token(self):
        """Test updating a user with no token in the request"""

        response = self.update_user(self.user_update)
        self.assertEqual(response.status_code, 403)
        msg = "Authentication credentials were not provided."
        self.assertEqual(response.data["detail"], msg)

    def test_update_user_invalid_token(self):
        """Test updating a user with an expired or invalid token"""

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.invalid_token)
        response = self.update_user(self.user_update)
        self.assertEqual(response.status_code, 403)
        msg = "Invalid token. Token decode failed"
        self.assertEqual(response.data["detail"], msg)

    def test_update_user_short_token(self):
        """Test updating a user with an invalid length token"""

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.invalid_token2)
        response = self.update_user(self.user_update)
        self.assertEqual(response.status_code, 403)
        msg = "Invalid token. Token decode failed"
        self.assertEqual(response.data["detail"], msg)

    def test_update_non_existent_user(self):
        """Test updating a user who doesn't exist"""

        self.token = self.get_user_token()
        self.email = self.user['email']
        User.objects.get(email=self.email).delete()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.update_user(self.user_update)
        self.assertEqual(response.status_code, 403)
        msg = "No user matching this token"
        self.assertEqual(response.data["detail"], msg)

    def test_update_user_no_bearer(self):
        """Test updating a user without prefix authorisation in the header"""

        self.token = self.get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.update_user(self.user_update)
        self.assertEqual(response.status_code, 403)
        msg = "Invalid authorization header"
        self.assertEqual(response.data["detail"], msg)

    def test_update_user_wrong_prefix(self):
        """Test updating user with wrong prefix authorisation in the header"""

        self.token = self.get_user_token()
        self.client.credentials(HTTP_AUTHORIZATION='Test ' + self.token)
        response = self.update_user(self.user_update)
        self.assertEqual(response.status_code, 403)
        msg = "Use a Bearer Token"
        self.assertEqual(response.data["detail"], msg)
