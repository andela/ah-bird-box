from rest_framework.views import status
from django.urls import reverse
from .base_test import TestConfiguration


class TestPasswordUpdate(TestConfiguration):

    def setUp(self):
        super().setUp()
        self.token = self.get_token_from_email()
        self.password_update_url = reverse(
            'authentication:update_password', kwargs={'token': self.token})

    def test_if_passwords_do_not_match(self):
        response = self.client.put(
            self.password_update_url, data=self.unmatched_passwords,
            format='json')
        message = b"Sorry, your passwords do not match"
        self.assertIn(message, response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_password_update_is_successful(self):
        response = self.client.put(
            self.password_update_url, data=self.passwords, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(b'Your password has been reset successfully',
                      response.content)
