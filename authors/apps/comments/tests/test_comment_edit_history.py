from .base_test import BaseTest
from rest_framework import status
from rest_framework.test import APIClient


class TestsCommentsHistory(BaseTest):

    def http_200_ok(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def http_403_forbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def http_404_not_found(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_comment_history_authenticated(self):
        """
        Test if an authenticated user can retrieve edit history of their
        comments
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(
            self.sample_comment, self.sample_article)
        comment_id = str(res.data['id'])
        url = self.comment_url("my-data") + comment_id + '/'
        response = self.client.put(
            url,
            self.sample_updated_comment,
            format='json'
        )
        url = self.comment_url("my-data") + comment_id + '/' + 'history/'
        response = self.client.get(url)
        self.http_200_ok(response)
        self.assertIn('Comment Edit History', response.data)

    def test_retrieve_comment_history_unauthenticated(self):
        """
        Test if an unauthenticated user can retrieve edit history of
        comments
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(
            self.sample_comment, self.sample_article)
        comment_id = str(res.data['id'])
        url = self.comment_url("my-data") + comment_id + '/'
        self.client.put(
            url,
            self.sample_updated_comment,
            format='json'
        )
        self.client = APIClient()
        url = self.comment_url("my-data") + comment_id + '/' + 'history/'
        response = self.client.get(url)
        self.http_403_forbidden(response)
        self.assertEqual(response.data
                         ['detail'], "Authentication credentials were not provided.") # noqa

    def test_retrieve_history_non_existent_comment(self):
        """
        Test if a user cannot retrieve the history of a non-existent comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        url = self.comment_url("my-data") + '/1000' + 'history/'
        response = self.client.get(url)
        self.http_404_not_found(response)

    def test_retrieve_history_missing_article(self):
        """
        This method tests a fetch on a non-existant article
        """
        self.authenticate_user(self.sample_user)
        url = self.comment_url("my-data-2") + '/1' + 'history/'
        response = self.client.get(url)
        self.http_404_not_found(response)
