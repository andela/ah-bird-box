from rest_framework import status

from authors.apps.authentication.tests.base_test import TestConfiguration


class CreateUserProfile(TestConfiguration):

    def test_get_user_profile(self):
        """
        Test user can view profile
        """
        token = self.get_user_token()
        response = self.client.get(
            self.user_profile_url,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'gracie')

    def test_view_all_users_profiles(self):
        """Test that a user can view all user profiles"""
        token = self.get_user_token()
        response = self.client.get(
            self.all_profiles_url,
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_that_a_user_can_edit_their_profile(self):
        """Tests the edit profile functionality"""
        token = self.get_user_token()
        response = self.client.put(
            self.edit_profile_url("gracie"),
            self.update_profile,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['company'], "Andela")

    def test_that_a_user_cannot_edit_another_users_profile(self):
        """Tests that a user can only edit their profile"""
        token = self.get_user_token()
        self.register_user(data=self.user2)

        response = self.client.put(
            self.edit_profile_url("JohnDoe"),
            self.update_profile,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertIn(response.data['detail'], "Edit permission denied")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
