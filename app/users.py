"""This module manages the users"""
USERS = {}

class User(object):
    """This class manages the app users"""

    def __init__(self, email=None, username=None, password=None):
        """Creates and instance of a user"""
        self.email = email
        self.username = username
        self.password = password

    def add_user(self, email, username, password):
        """This method adds a new user to the app"""
        if email not in USERS:
            USERS[email] = {"email": email, "username": username, "password": password}
            return "User added successfully."
        return "Sorry, that email is already registered."

    def get_user(self, email, password):
        """This method gets an existing user from the users's list"""
        # Get an existing user
        # First check whether user account exists
        if email in USERS:
            current_user = USERS[email]
            # confirm that correct password was entered
            if current_user["password"] == password:
                return current_user
            return "Password error!"
        return "User not found!"
