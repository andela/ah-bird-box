from rest_framework import status

from authors.apps.authentication.tests.base_test import TestConfiguration


class TestEmailVerification(TestConfiguration):
    """test whether a user receives a verification email on signup"""

    def test_an_email_is_sent_on_registration(self):
        """test to check whether user is successfully registered"""
        response = self.register_user(data=self.user)
        self.assertEqual(
            response.data['message'],
            "User registered successfully."
            " Check your email to activate your account.")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_verify_email(self):
        """test to check if email is verified"""
        response = self.register_user(data=self.user)
        token = response.data['user_info']['token']
        # hit the api endpoint
        verify_url = "http://127.0.0.1:8000/api/users/verify/{}".format(token)
        res = self.client.get(verify_url)
        message = 'Email verified successfully'
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(message.encode(), res.content)
