""" This is the testing suite for the Users Module """

import unittest

from app.users import User
from app.users import USERS

class UserManagementTestCase(unittest.TestCase):
    """This class tests the users.py"""

    def setUp(self):
        """Set up test"""
        self.user = User()
        self.current_users = USERS
        self.user_email = "fn@yummy.io"
        self.username = "fena"
        self.password = "fenamenal"

    def test_user_creation(self):
        """Testing user is added successfully"""
        test_user = self.user.add_user(self.user_email, self.username, self.password)
        self.assertEqual(test_user, "User added successfully.")

    def test_user_duplication(self):
        """Test when user attempts to create account with existing email"""
        duplicate_user = self.user.add_user(self.user_email, "some_guy", "some_pass")
        self.assertEqual(duplicate_user, "Sorry, that email is already registered.")

    def test_user_retrieval(self):
        """Testing the User get_user method"""
        retrieved_user = self.user.get_user(self.user_email, self.password)
        self.assertEqual(self.user_email, retrieved_user["email"])

    def test_non_existent_user(self):
        """Testing user retrival for a user that doesn't exist"""
        retrieved_user = self.user.get_user("user@email.me", self.password)
        self.assertEqual(retrieved_user, "User not found!")
