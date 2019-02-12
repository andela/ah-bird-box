from .base_test import TestBaseCase

from rest_framework import status


class TestArticle(TestBaseCase):
    def base_articles(self, message, response):
        self.assertIn(message.encode(), response.content)

    def authorized_post_request(self, url):
        token = self.login_user()
        response = self.client.post(
            url, self.article, format='json',
            HTTP_AUTHORIZATION='Bearer ' + token)
        return response

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
        response = self.authorized_post_request(self.create_list_article_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_create_article_duplicate_title(self):
        """
        This method checks if an article with a duplicate
        title can be created
        """
        self.authorized_post_request(self.create_list_article_url)
        response = self.authorized_post_request(self.create_list_article_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_create_articles_unauthorized(self):
        """
        This method ensures that an unauthorized user cannot create an article
        """
        response = self.client.post(self.create_list_article_url,
                                    self.article, format='json')
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided."
        self.base_articles(message, response)

    def test_fetch_articles(self):
        """
        This method tests if users can retrieve articles
        """
        self.create_article()
        response = self.client.get(self.create_list_article_url,
                                   format='json')
        self.http_200_ok(response)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_authorized_user_view_articles(self):
        """
        This method tests if authenticated users can view articles
        """
        response = self.client.get(
            self.single_article_url(self.create_article()), format='json',
            HTTP_AUTHORIZATION='Bearer ' + self.login_user())
        self.http_200_ok(response)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_create_article_missing_title(self):
        """
        This method tests if a user can post without a title
        """
        self.article.pop('title')
        response = self.authorized_post_request(self.create_list_article_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = "Title is required"
        self.base_articles(message, response)

    def test_article_update(self):
        """
        This method checks if a user can update an existing articles
        """
        response = self.authorized_post_request(self.create_list_article_url)
        slug = response.data['slug']
        token = self.login_user()
        res = self.client.put(self.single_article_url(slug),
                              self.updated_article, format='json',
                              HTTP_AUTHORIZATION="Bearer "+token)
        self.assertIn(b"Updated Title", res.content)
        self.http_200_ok(res)
        message = "Test description for the article"
        self.base_articles(message, response)

    def test_unauthorised_user_update(self):
        """
        This method tests if unauthorized user can update existing articles
        """
        slug = self.create_article()
        response = self.client.put(self.single_article_url(slug),
                                   self.updated_article,
                                   format='json')
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided."
        self.base_articles(message, response)

    def test_user_can_delete(self):
        """
        This method tests if a user can delete articles
        """
        response = self.authorized_post_request(self.create_list_article_url)
        slug = response.data['slug']
        response = self.client.delete(
            self.single_article_url(slug), format='json',
            HTTP_AUTHORIZATION='Bearer ' +
            self.login_user())
        message = "Article Deleted Successfully"
        self.base_articles(message, response)
        self.http_200_ok(response)

    def test_unauthorised_user_delete(self):
        """
        This method tests if a user can delete other
        users articles
        """
        slug = self.create_article()
        response = self.client.delete(self.single_article_url(slug),
                                      format='json')
        self.http_403_forbidden(response)
        message = "Authentication credentials were not provided"
        self.base_articles(message, response)

    def test_view_missing_article(self):
        """
        This method tests a fetch on a non-existant article
        """
        response = self.client.get(
            self.single_article_url("slug-never-to-be-created-56cjgcaG"),
            format='json',
            HTTP_AUTHORIZATION='Bearer ' + self.login_user())
        self.http_400_bad_request(response)
        message = "No article found for the slug given"
        self.base_articles(message, response)

    def test_update_missing_article(self):
        """
        This method checks if a user can update an existing articles
        """
        response = self.authorized_post_request(self.create_list_article_url)
        token = self.login_user()
        response = self.client.put(self.single_article_url("missing-article"),
                                   self.updated_article,
                                   format='json',
                                   HTTP_AUTHORIZATION="Bearer "+token)
        self.http_400_bad_request(response)
        message = "No article found for the slug given"
        self.base_articles(message, response)

    def test_delete_missing_article(self):
        """
        This method tests if a user can delete a non-existent
        article
        """
        response = self.authorized_post_request(self.create_list_article_url)
        response = self.client.delete(
            self.single_article_url("missing-article"), format='json',
            HTTP_AUTHORIZATION='Bearer ' +
            self.login_user())
        self.http_400_bad_request(response)
        message = "No article found for the slug given"
        self.base_articles(message, response)
