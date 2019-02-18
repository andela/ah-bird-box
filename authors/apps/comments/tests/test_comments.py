from .base_test import BaseTest
from rest_framework import status


class TestComments(BaseTest):
    """
    Comments Tests
    """

    def test_unauthenticated_user_cannot_comment(self):
        """
        Tests if a user who is not authorized can comment
        """
        self.create_article(self.sample_article)
        response = self.create_comment(
            self.sample_comment, self.sample_article)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")

    def test_user_cannot_post_empty_comment(self):
        """
        Test that a user cannot post an empty comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        response = self.create_comment(
            self.sample_null_comment_body, self.sample_article)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['errors']["body"][0], "This field may not be blank.")

    def test_user_can_post_comment(self):
        """
        Test if a user can post a comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        response = self.create_comment(
            self.sample_comment, self.sample_article)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_can_post_child_comment(self):
        """
        Test if a user can post a child comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(
            self.sample_comment, self.sample_article)
        comment_id = str(object=res.data['id'])
        url = self.comment_url("my-data") + comment_id + '/'
        res = self.client.post(url, data={
            'body': 'This is a child comment'
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_can_retrieve_all_comments(self):
        """
        Test if user can retrieve all comments
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        self.create_comment(self.sample_comment, self.sample_article)
        response = self.client.get(self.comment_url("my-data"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_one_comment(self):
        """
        Test if user can retrieve one comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(self.sample_comment, self.sample_article)
        comment_id = str(object=res.data['id'])
        url = self.comment_url("my-data") + comment_id + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_retrieve_non_existent_comment(self):
        """
        Test user can retrieve a non-resistent comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(
            self.sample_comment, self.sample_article)
        comment_id = str(object=res.data['id'])
        url = self.comment_url("my-data") + comment_id + '/'
        self.client.delete(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('comment', response.data)
        self.assertIn('commentsCount', response.data)

    def test_user_can_update_comment(self):
        """
        Test user can update their own comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(
            self.sample_comment, self.sample_article)
        comment_id = str(object=res.data['id'])
        url = self.comment_url("my-data") + comment_id + '/'
        response = self.client.put(
            url,
            self.sample_updated_comment,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['comment']['message'],
            "Comment was successfully updated"
        )

    def test_unauthorized_update_comment(self):
        """
        Test a user cannot update other user's comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(
            self.sample_comment, self.sample_article)
        self.authenticate_user(self.sample_wrong_user_details)
        comment_id = str(object=res.data['id'])
        url = self.comment_url("my-data") + comment_id + '/'
        response = self.client.put(
            url,
            self.sample_updated_comment,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['comment']
                         ['message'], "Sorry, you are not authorized to update this comment") # noqa

    def test_unauthorized_delete_comment(self):
        """
        Test a user cannot update other user's comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(
            self.sample_comment, self.sample_article)
        self.authenticate_user(self.sample_wrong_user_details)
        comment_id = str(object=res.data['id'])
        url = self.comment_url("my-data") + comment_id + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['comment']
                         ['message'], "Sorry, you are not authorized to delete this comment") # noqa

    def test_user_can_delete_a_comment(self):
        """
        Test if user can delete a comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        res = self.create_comment(self.sample_comment, self.sample_article)
        comment_id = str(object=res.data['id'])
        url = self.comment_url("my-data") + comment_id + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment']
                         ['message'], "Comment was successfully deleted")

    def test_delete_non_existent_comment(self):
        """
        Test if user can delete a comment
        """
        self.authenticate_user(self.sample_user)
        self.create_article(self.sample_article)
        url = self.comment_url("my-data") + '3/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['comment']
                         ['message'], "Sorry, comment was not found")
