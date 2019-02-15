# module import
from authors.apps.rating.tests.base_test import TestConfiguration


class TestRating(TestConfiguration):

    def test_get_ratings_anonymous(self):
        """
        Test that a non-authenticated user can view an article's ratings
        """
        response = self.get_ratings(url=self.ratings_url)
        self.assertEqual(response.status_code, 200)

    def test_get_ratings_authenticated(self):
        """
        Test that an authenticated user can view an article's ratings
        """
        response = self.get_ratings(
            is_authenticated=True, url=self.ratings_url)
        self.assertEqual(200, response.status_code)

    def test_get_ratings_unavailable_article(self):
        """
        Test it raises an error when an article is not found
        """
        response = self.get_ratings(is_found=False, url=self.ratings_url2)
        self.assertIn('errors', response.data)
        self.assertEqual(404, response.status_code)

    def test_rate_article_anonymous(self):
        """
        Test that an anonymous user cannot rate an article
        """
        response = self.rate(is_authenticated=False, stars=self.stars,
                             url=self.ratings_url)
        self.assertIn('detail', response.data)
        self.assertEqual(403, response.status_code)

    def test_rate_article_authenticated(self):
        """
        Test that an authenticated user can rate an article
        """
        response = self.rate(stars=self.stars, url=self.ratings_url)
        self.assertEqual(201, response.status_code)
        self.assertIn('user', response.data)
        self.assertIn('stars', response.data)

    def test_rate_article_authenticated_wrong_data(self):
        """
        Test a star rating more than 5
        """
        response = self.rate(stars=self.stars2, url=self.ratings_url)
        self.assertEqual(400, response.status_code)
        self.assertIn(
            'Star ratings should be from 1 and 5 stars',
            response.data['errors'])

    def test_rate_unavailable_article(self):
        """
        Test that when an article is not found an error is displayed
        """
        response = self.rate(is_found=False, stars=self.stars,
                             url=self.ratings_url2)
        self.assertIn('Article not found', response.data['errors'])
        self.assertEqual(400, response.status_code)

    def test_rate_my_own_article(self):
        """
        Test that an author cannot rate their own article
        """
        response = self.rate(user=self.user2, stars=self.stars,
                             url=self.ratings_url)
        self.assertIn('You cannot rate your own article',
                      response.data['errors'])
        self.assertEqual(400, response.status_code)

    def test_that_articles_show_ratings(self):
        """
        Test that while getting an article, there are averageRating and
        ratingsCount
        """
        self.assertDictContainsSubset({"averageRating": None,
                                       "ratingsCount": 0},
                                        self.client.get(self.one_article_url).data)  # noqa
