import json

from rest_framework import status

from authors.apps.articles.tests.base_test import TestBaseCase


class TagsTest(TestBaseCase):

    def base_articles(self, message, response):
        self.assertIn(message.encode(), response.content)

    def http_200_ok(self, response, message):
        self.base_articles(message, response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def http_201_created(self, response, message):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.base_articles(message, response)

    def http_403_forbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_users_cannot_create_article_with_tags(self):
        """Tests whether unauthorized users can create tags"""
        url = self.create_list_article_url
        response = self.client.post(url, data=self.article, format='json')
        message = "Authentication credentials were not provided"
        self.base_articles(message, response)
        self.http_403_forbidden

    def test_users_can_create_article_with_tags(self):
        """Tests whether a user can create article with tags"""
        self.authenticate_user(self.test_user)
        response = self.create_article()
        message = '"tags": ["test", "tags"]'
        self.http_201_created(response, message)

    def test_tags_are_created_as_slugs(self):
        self.article['tags'].extend(["THIS IS A TAG"])
        self.authenticate_user(self.test_user)
        response = self.create_article()
        self.assertIn('this-is-a-tag', json.dumps(response.data))

    def test_user_cannot_create_tag_with_special_characters(self):
        self.article['tags'].extend(["Tag with special characters @#$"])
        self.authenticate_user(self.test_user)
        response = self.create_article()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        message = "Tag cannot have special characters"
        self.base_articles(message, response)

    def test_user_can_create_article_without_tag(self):
        """Test whether a user can create an article without a tag"""
        del self.article['tags']
        self.authenticate_user(self.test_user)
        response = self.create_article()
        message = '"tags": []'
        self.http_201_created(response, message)

    def test_user_can_retrieve_all_tags(self):
        """Tests whether a user can retrieve all tags"""
        self.authenticate_user(self.test_user)
        self.create_article()
        url = self.get_tags_url
        response = self.client.get(url)
        message = 'tags":["test","tags"]'
        self.http_200_ok(response, message)

    def test_user_can_retrieve_article_with_tags(self):
        """Tests whether a user can retrieve an article with tags"""
        self.authenticate_user(self.test_user)
        self.create_article()
        response = self.client.get(self.create_list_article_url,
                                   format='json')
        message = '"tags": ["test", "tags"]'
        self.http_200_ok(response, message)
