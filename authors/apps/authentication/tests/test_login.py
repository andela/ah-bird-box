# module import
from rest_framework import status
from authors.apps.authentication.tests.base_test import TestConfiguration


class TestLogin(TestConfiguration):

    def test_successful_login(self):
        """test if login is successful """
        self.register_user(data=self.user)
        response = self.user_login_req(data=self.user_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "graceunah@gmail.com")

    def test_login_email_does_not_exist(self):
        """ test login with non existing email """
        self.register_user(data=self.user)
        self.user_login["user"]["email"] = "chixy.com"
        response = self.user_login_req(data=self.user_login)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors']['error'][0],
                         "A user with this email and password was not found.")

    def test_login_with_empty_email_field(self):
        """ test login with empty email """

        response = self.register_user(data=self.user_empty_email)
        self.assertEqual(
            response.data['errors']['email'][0],
            "This field may not be blank.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_empty_password_field(self):
        """ test login with empty password """
        response = self.register_user(data=self.user_empty_password)
        self.assertEqual(
            response.data['errors']['password'][0],
            "This field may not be blank.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
