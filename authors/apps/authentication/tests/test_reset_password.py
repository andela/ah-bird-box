from rest_framework import status
from django.core import mail

from .base_test import TestConfiguration


class TestPasswordReset(TestConfiguration):

    def test_if_email_actually_exists(self):
        response = self.client.post(self.password_reset_url,
                                    data={"email": "ahbirdbox03@gmail.com"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(
            b'Sorry, user with this email does not exist',
            response.content)

    def test_if_no_email_has_been_provided(self):
        response = self.client.post(self.password_reset_url,
                                    data={"email": ""},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'Please provide an email address', response.content)

    def test_email_successfully_sent(self):
        self.register_user(data=self.user)
        response = self.client.post(self.password_reset_url,
                                    data={"email": "graceunah@gmail.com"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            b'Check your inbox for a link to reset your password',
            response.content)
        self.assertTrue(len(mail.outbox) >= 1)
