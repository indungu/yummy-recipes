"""This module manages the users"""
USERS = {
    "in@yummy.io": {"email": "in@yummy.io", "username": "indungu", "password": "pass2017"},
    "cb@yummy.io": {"email": "cb@yummy.io", "username": "cbreezy", "password": "questions"}
}

class User(object):
    """This class manages the app users"""

    def __init__(self, email=None, username=None, password=None):
        """Creates and instance of a user"""
        self.email = email
        self.username = username
        self.password = password

    def add_user(self, email, username, password):
        """This method adds a new user to the app"""
        current_users = USERS.keys()
        if email not in current_users:
            new_user = {"email": email, "username": username, "password": password}
            USERS[email] = new_user
            return USERS
        elif email in USERS.keys():
            return "Sorry, that email is already taken, choose a different one"

    def get_user(self, email, password):
        """This method gets an existing user from the users's list"""
