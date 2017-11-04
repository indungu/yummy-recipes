""" This is the testing suite for the Users Module """

import unittest

from app.users import User
from app.users import USERS

class UserManagementTestCase(unittest.TestCase):
    """This class tests the users.py"""

    def setUp(self):
        """Set up test"""
        self.user = User("fn@yummy.io", "fena", "fenamenal")
        self.user_email = self.user.email
        self.current_users = USERS
    def test_user_creation(self):
        """Testing user is added successfully"""
        test_user = self.user.add_user()
        self.assertEqual(test_user, "User added successfully.")

    def test_user_duplication(self):
        """Test when user attempts to create account with existing email"""
        duplicate_user = self.user.add_user()
        self.assertEqual(duplicate_user, "Sorry, that email is already registered.")

    def test_user_retrieval(self):
        """Testing the User get_user method"""
        retrieved_user = self.user.get_user()
        self.assertEqual(self.user_email, retrieved_user[0])
