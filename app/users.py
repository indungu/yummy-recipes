"""This module manages the users"""
USERS = {
    "indungu": {"email": "in@yummy.io", "username": "indungu", "password": "pass2017"},
    "cbreezy": {"email": "cb@yummy.io", "username": "cbreezy", "password": "questions"}
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
        if username not in current_users:
            new_user = {"email": email, "username": username, "password": password}
            USERS[username] = new_user
            return USERS
        elif username in USERS.keys():
            return "Sorry, that username is already taken, choose a different one"    
