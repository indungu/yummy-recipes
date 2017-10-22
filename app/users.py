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
        current_users = USERS.keys()
        if email not in current_users:
            USERS[email] = {"email": email, "username": username, "password": password}
            return USERS
        elif email in USERS.keys():
            return "Sorry, that email is already registered."

    def get_user(self, email, password, user_list):
        """This method gets an existing user from the users's list"""
        # Get an existing user
        # First check whether user account exists
        if email in USERS.keys():
            current_user = USERS[email]
            # confirm that correct password was entered
            if current_user["password"] == password:
                return current_user
        # Get an instance user
        else:
            if email in user_list.keys():
                instance_user = user_list[email]
                if instance_user["email"] == email:
                    return user_list[email]
            return USERS
