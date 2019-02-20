from rest_framework.test import APIClient

from .base_test import TestBaseCase


class TestDislikes(TestBaseCase):
    def test_dislike_unauthenticated_user(self):
        self.authenticate_user(self.test_user)
        article_details = self.create_article()
        slug = article_details.data['slug']
        self.client = APIClient()
        response = self.dislike_article(slug)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            "Authentication credentials were not provided.",
            response.data['detail'])

    def test_dislike_authenticated_user(self):
        self.authenticate_user(self.test_user)
        article_details = self.create_article()
        slug = article_details.data['slug']
        response = self.dislike_article(slug)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.data['dislikes_count'])

    def test_dislike_unfound_article(self):
        self.authenticate_user(self.test_user)
        slug = self.wrong_slug
        response = self.dislike_article(slug)
        self.assertEqual(404, response.status_code)
        self.assertEqual(
            "An article with this slug does not exist",
            response.data['detail'])

    def test_dislike_liked_article(self):
        self.authenticate_user(self.test_user)
        article_details = self.create_article()
        slug = article_details.data['slug']
        response = self.like_article(slug)
        response = self.dislike_article(slug)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.data['likes_count'])
        self.assertEqual(1, response.data['dislikes_count'])

    def test_dislike_disliked_article(self):
        self.authenticate_user(self.test_user)
        article_details = self.create_article()
        slug = article_details.data['slug']
        response = self.dislike_article(slug)
        response = self.dislike_article(slug)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, response.data['dislikes_count'])
        self.assertEqual(0, response.data['likes_count'])
