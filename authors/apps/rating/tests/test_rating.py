# module import
from rest_framework.test import APIClient
from django.urls import reverse

from authors.apps.rating.tests.base_test import TestConfiguration


class TestRating(TestConfiguration):

    def test_get_ratings_anonymous(self):
        """
        Test that a non-authenticated user can view an article's ratings
        """
        article_details = self.create_article()
        self.client = APIClient()
        response = self.get_ratings(article_details['slug'])
        self.assertEqual(response.status_code, 200)

    def test_get_ratings_authenticated(self):
        """
        Test that an authenticated user can view an article's ratings
        """
        article_details = self.create_article()
        response = self.get_ratings(article_details['slug'])
        self.assertEqual(response.status_code, 200)

    def test_get_ratings_unavailable_article(self):
        """
        Test it raises an error when an article is not found
        """
        self.authenticate_user(self.user)
        response = self.get_ratings(self.wrong_slug)
        self.assertIn('errors', response.data)
        self.assertEqual(404, response.status_code)

    def test_rate_article_anonymous(self):
        """
        Test that an anonymous user cannot rate an article
        """
        article_details = self.create_article()
        self.client = APIClient()
        response = self.rate(slug=article_details['slug'], stars=self.stars)
        self.assertIn('detail', response.data)
        self.assertEqual(403, response.status_code)

    def test_rate_article_authenticated(self):
        """
        Test that an authenticated user can rate an article
        """
        article_details = self.create_article()
        self.authenticate_user(self.user2)
        response = self.rate(slug=article_details['slug'], stars=self.stars)
        self.assertEqual(201, response.status_code)
        self.assertIn('user', response.data)
        self.assertIn('stars', response.data)

    def test_rate_article_authenticated_wrong_data(self):
        """
        Test a star rating more than 5
        """
        article_details = self.create_article()
        self.authenticate_user(self.user2)
        response = self.rate(slug=article_details['slug'], stars=self.stars2)
        self.assertEqual(400, response.status_code)
        self.assertIn(
            'Star ratings should be from 1 and 5 stars',
            response.data['errors'])

    def test_rate_unavailable_article(self):
        """
        Test that when an article is not found an error is displayed
        """
        self.authenticate_user(self.user2)
        response = self.rate(slug=self.wrong_slug, stars=self.stars)
        self.assertIn('Article not found', response.data['errors'])
        self.assertEqual(400, response.status_code)

    def test_rate_my_own_article(self):
        """
        Test that an author cannot rate their own article
        """
        article_details = self.create_article()
        response = self.rate(slug=article_details['slug'], stars=self.stars)
        self.assertIn('You cannot rate your own article',
                      response.data['errors'])
        self.assertEqual(400, response.status_code)

    def test_that_articles_show_ratings(self):
        """
        Test that while getting an article, there are averageRating and
        ratingsCount
        """
        article_details = self.create_article()
        self.one_article_url = reverse("articles:article-details",
                                       kwargs={"slug": article_details['slug']})  # noqa
        self.assertDictContainsSubset({"averageRating": None,
                                       "ratingsCount": 0},
                                        self.client.get(self.one_article_url).data)  # noqa
