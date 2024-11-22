from django.test import TestCase
from users.models import User

class UserTest(TestCase):
    def test_user_str_method(self):
        test_user = User(first_name="Bob", email='bob@sky.pro')
        self.assertEqual(str(test_user), "Bob")