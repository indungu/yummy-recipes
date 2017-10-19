""" This is the testing suite for the Users Module """

import unittest

from app.users import User

class UserManagemertTestCase(unittest.TestCase):
    """This class tests the users.py"""

    def test_user_creation(self):
        """test user is added successfully"""
        new_user = User()
