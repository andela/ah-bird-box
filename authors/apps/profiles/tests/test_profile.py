from rest_framework import status

# local imports

from authors.apps.profiles.tests.base_test import TestConfiguration


class CreateUserProfile(TestConfiguration):

    def test_get_user_profile(self):
        """
        Test user can view profile
        """
        response = self.register_user(data=self.user)
        self.authorize_user(self.user_login_details)
        username = self.user['user']['username']
        token = response.data['user_info']['token']
        url = '/api/profiles/' + username
        response = self.client.get(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_all_users_profiles(self):
        """Test that a user can view all user profiles"""
        response = self.register_user(data=self.user)
        self.authorize_user(self.user_login_details)
        token = response.data['user_info']['token']
        url = '/api/profiles/'
        response = self.client.get(
            url,
            content_type='application/json',
            HTTP_AUTHORIZATION='Token ' + token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_a_user_can_edit_their_profile(self):
        """Tests the edit profile functionality"""
        self.authorize_user(self.user_login_details)
        url = self.profiles_url + \
            '{}'.format(self.user['user']['username']) + "/"
        response = self.client.patch(url, data=self.update_profile)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_a_user_cannot_edit_another_users_profile(self):
        """Tests that a user can only edit their profile"""
        self.authorize_user(self.user_login_details)
        self.register_user(self.user2)
        url = self.profiles_url + \
            '{}'.format(self.user2['user']['username']) + "/"
        response = self.client.patch(url, data=self.update_profile)
        message = "Edit permission denied"
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
