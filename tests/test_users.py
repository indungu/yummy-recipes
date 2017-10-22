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
        """testing user is added successfully"""
        self.assertTrue(self.user_email in self.test_user.keys())

    def test_user_duplication(self):
        """Test when user attempts to create account with existing email"""
        duplicate_user = self.new_user.add_user(self.user_email, "some_guy", "some_pass")
        self.assertEqual(duplicate_user, "Sorry, that email is already registered.")

    def test_user_retrieval(self):
        """Testing the User get_user method"""
        new_user = self.test_user
        retrieved_user = self.new_user.get_user(self.user_email, self.password, new_user)
        self.assertEqual(self.user_email, retrieved_user["email"])
