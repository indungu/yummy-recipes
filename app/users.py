"""This module manages the users"""
from werkzeug.security import generate_password_hash
USERS = {}

class User(object):
    """This class manages the app users"""

    def __init__(self, email, username, password):
        """Creates and instance of a user"""
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def add_user(self):
        """This method adds a new user to the USERS dictionary"""
        if self.email not in USERS:
            USERS[self.email] = self
            return "User added successfully."
        return "Sorry, that email is already registered."

    def get_user(self):
        """This method gets an existing user from the users's list"""
        return (self.email, self.password)

    def delete_user(self):
        """This method deletes a user"""
        USERS.pop(self.email)
