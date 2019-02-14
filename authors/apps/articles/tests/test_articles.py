from rest_framework.test import APIClient
from rest_framework import status

from .base_test import TestBaseCase


class TestArticle(TestBaseCase):
    def base_articles(self, message, response):
        self.assertIn(message.encode(), response.content)

    def http_200_ok(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def http_403_forbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def http_400_bad_request(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_authorized(self):
        """
        This method checks if an uthorized user can create an article
        """
        self.authenticate_user(self.test_user)
        response = self.create_article()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_create_article_duplicate_title(self):
        """
        This method checks if an article with a duplicate
        title can be created
        """
        self.authenticate_user(self.test_user)
        self.create_article()
        response = self.create_article()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_create_articles_unauthorized(self):
        """
        This method ensures that an unauthorized user cannot create an article
        """
        response = self.create_article()
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided."
        self.base_articles(message, response)

    def test_fetch_articles(self):
        """
        This method tests if users can retrieve articles
        """
        self.authenticate_user(self.test_user)
        self.create_article()
        response = self.client.get(self.create_list_article_url,
                                   format='json')
        self.http_200_ok(response)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_create_article_missing_title(self):
        """
        This method tests if a user can post without a title
        """
        self.authenticate_user(self.test_user)
        self.article.pop('title')
        response = self.create_article()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = "Title is required"
        self.base_articles(message, response)

    def test_article_update(self):
        """
        This method checks if a user can update an existing articles
        """
        self.authenticate_user(self.test_user)
        response = self.create_article()
        slug = response.data['slug']
        res = self.client.put(self.single_article_url(slug),
                              self.updated_article, format='json')
        self.assertIn(b"Updated Title", res.content)
        self.http_200_ok(res)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_unauthorised_user_update(self):
        """
        This method tests if unauthorized user can update existing articles
        """
        self.authenticate_user(self.test_user)
        response = self.create_article()
        self.client = APIClient()
        response = self.client.put(
            self.single_article_url(response.data['slug']),
            self.updated_article, format='json')
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided."
        self.base_articles(message, response)

    def test_user_can_delete(self):
        """
        This method tests if a user can delete articles
        """
        self.authenticate_user(self.test_user)
        response = self.create_article()
        slug = response.data['slug']
        response = self.client.delete(
            self.single_article_url(slug), format='json')
        message = "Article Deleted Successfully"
        self.base_articles(message, response)
        self.http_200_ok(response)

    def test_unauthorised_user_delete(self):
        """
        This method tests if a user can delete other
        users articles
        """
        self.authenticate_user(self.test_user)
        response = self.create_article()
        slug = response.data['slug']
        self.client = APIClient()
        response = self.client.delete(self.single_article_url(slug),
                                      format='json')
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided"
        self.base_articles(message, response)

    def test_view_missing_article(self):
        """
        This method tests a fetch on a non-existant article
        """
        self.authenticate_user(self.test_user)
        response = self.client.get(
            self.single_article_url("slug-never-to-be-created-56cjgcaG"),
            format='json')
        self.http_400_bad_request(response)
        message = "No article found for the slug given"
        self.base_articles(message, response)

    def test_update_missing_article(self):
        """
        This method checks if a user can update an existing articles
        """
        self.authenticate_user(self.test_user)
        response = self.create_article()
        response = self.client.put(self.single_article_url("missing-article"),
                                   self.updated_article)
        self.http_400_bad_request(response)
        message = "No article found for the slug given"
        self.base_articles(message, response)

    def test_delete_missing_article(self):
        """
        This method tests if a user can delete a non-existent
        article
        """
        self.authenticate_user(self.test_user)
        response = self.create_article()
        response = self.client.delete(
            self.single_article_url("missing-article"), format='json')
        self.http_400_bad_request(response)
        message = "No article found for the slug given"
        self.base_articles(message, response)
