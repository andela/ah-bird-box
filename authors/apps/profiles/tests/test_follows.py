from rest_framework import status

from authors.apps.authentication.tests.base_test import TestConfiguration


class FollowUnfollowTestCase(TestConfiguration):
    """
    This class creates a testcase for follow and unfollow functionality
    """

    def test_successful_follow(self):
        """Test whether API user can follow another successfully"""
        token = self.get_user_token()
        self.register_user(data=self.user2)
        response = self.follow_user("JohnDoe", token)
        self.assertEqual(response.data['message'],
                         "You are now following JohnDoe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_unavailable_user(self):
        """Test whether API user can follow an unavailable user"""
        token = self.get_user_token()
        response = self.follow_user("333", token)
        self.assertEqual(response.data['error'],
                         "User not found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_yourself(self):
        """Test whether API user can follow oneself"""
        token = self.get_user_token()
        response = self.follow_user("gracie", token)
        self.assertEqual(response.data['error'],
                         "You cannot follow yourself")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_follow_user_already_followed(self):
        """Test whether API user can follow a user they already follow"""
        token = self.get_user_token()
        self.register_user(data=self.user2)
        self.follow_user("JohnDoe", token)
        response = self.follow_user("JohnDoe", token)
        self.assertEqual(response.data['error'],
                         "You already follow JohnDoe")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_successful_unfollow(self):
        """Test whether API user can unfollow a follower successfully"""
        token = self.get_user_token()
        self.register_user(data=self.user2)
        self.follow_user("JohnDoe", token)
        response = self.unfollow_user("JohnDoe", token)
        self.assertEqual(response.data['message'],
                         "You have successfully unfollowed JohnDoe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unfollow_unavailable_user(self):
        """Test whether API user can unfollow a follower successfully"""
        token = self.get_user_token()
        response = self.unfollow_user("UnavailableUser", token)
        self.assertEqual(response.data['error'],
                         "User not found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unfollow_nonfollower(self):
        """Test whether API user can unfollow a user they don't follow"""
        token = self.get_user_token()
        self.register_user(data=self.user2)
        response = self.unfollow_user("JohnDoe", token)
        self.assertEqual(response.data['error'],
                         "You do not follow JohnDoe")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_following(self):
        """Test whether API user can view follow list successfully"""
        token = self.get_user_token()
        self.register_user(data=self.user2)
        self.follow_user("JohnDoe", token)
        response = self.get_following("JohnDoe", token)
        self.assertIsInstance(response.data['Followers'], list)
        self.assertIsInstance(response.data['Following'], list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
