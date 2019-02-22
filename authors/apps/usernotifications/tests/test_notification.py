from django.urls import reverse
from django.core import mail
from django.conf import settings
from rest_framework import status

from .base_test import BaseTestCase


class NotificationsTestCase(BaseTestCase):
    """
    class for notification tests
    """

    def test_get_notification_when_article_created(self):
        """
        test user will get notification when followed
        """
        # assert no notifcations
        token = self.authenticate_user(self.follower)
        self.authenticate_user(self.article_author)

        follow_url = reverse("profile:follow", kwargs={'username': "testuser"})
        self.client.post(
            follow_url,
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.create_article()
        response1 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data["count"], 0)

    def test_send_email_notification(self):
        """
        test that email notification is sent
        """
        # empty the test outbox
        mail.outbox = []
        self.assertEqual(len(mail.outbox), 0)
        mail.send_mail(
            'Authors Haven Notifications', 'Here is the message.',
            settings.EMAIL_HOST_USER, ['gracieme@gmail.com'],
            fail_silently=False,
        )
        # test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject,
                         'Authors Haven Notifications')

    def test_unauthenticated_user_cannot_view_notifications(self):
        """
        test an authenticated user won't view notifications
        """
        response = self.client.get(reverse("notifications:all-notifications"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscribeUnsubscribeTestCase(BaseTestCase):
    """
    test class for subscribing and unsubscribing to notifications
    """
    def test_unsubscribe_from_in_app(self):
        """
        test user can unsubscribe from notifications
        test user can subscribe back to notifications
        """
        # test unsubscribe
        self.authenticate_user(self.article_author)
        response1 = self.client.post(
            self.subscribe_url, data=self.subscribe_data)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        msg = "You have successfully set email to True and app to True"
        self.assertEqual(
            response1.data['message'], msg)
