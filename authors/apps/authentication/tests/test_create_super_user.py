# local import
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base_test import TestConfiguration


class TestAdmin(TestConfiguration):
    def test_create_super_user(self):
        """ test create super user """
        the_admin = User.objects.create_superuser(
            'myuser',
            'myemail@test.com',
            'password'
        )
        self.assertEqual(the_admin.is_active, True)
        self.assertEqual(the_admin.is_staff, True)
        self.assertEqual(the_admin.is_superuser, True)
