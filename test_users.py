""" This is the testing suite for the Users Module """

import unittest

from app.users import User
from app.users import USERS

class UserManagementTestCase(unittest.TestCase):
    """This class tests the users.py"""

    def setUp(self):
        """Set up test"""
        self.new_user = User()
        self.current_users = USERS
        self.user_email = "fn@yummy.io"
        self.username = "fena"
        self.password = "fenamenal"
        self.test_user = self.new_user.add_user(self.user_email, self.username, self.password)

    def test_user_creation(self):
        """test user is added successfully"""
        self.assertTrue(self.user_email in self.test_user.keys())
