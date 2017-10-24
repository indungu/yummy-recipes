"""Routes testing suite."""

from unittest import TestCase

from app import APP
from app.users import User

class RoutesTestCase(TestCase):
    """This class contains all the test methods used for testing"""

    def login(self, email, password):
        """This method creates a login session"""
        return self.test_app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """This helper method clears a login session"""
        return self.test_app.get('/logout', follow_redirects=True)


    def setUp(self):
        """set up for each test"""
        self.test_app = APP.test_client()
        self.user_email = "in@user.me"
        self.username = "user"
        self.user_password = "password"
        self.user = User()

    def test_root_route(self):
        """Tests whether the root url opens"""
        reponse = self.test_app.get('/')
        self.assertEqual(reponse.status_code, 200)

    def test_signup_route(self):
        """Test if the signup route/url opens"""
        response = self.test_app.get('/signup')
        self.assertEqual(response.status_code, 200)
        response = self.test_app.post('/signup', data=dict(
            email=self.user_email, username=self.username, password=self.user_password
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        """Test if the login route/url opens"""
        response = self.test_app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_route_without_login(self):
        """When user is not authorized"""
        response = self.test_app.get('/dashboard')
        self.assertEqual(response.status_code, 302)

    def test_dashboard_route_with_login(self):
        """When user is authorized"""
        self.user.add_user(self.user_email, self.username, self.user_password)
        response = self.login(self.user_email, self.user_password)
        self.assertEqual(response.status_code, 200)

    def test_invalid_routes(self):
        """Test if invalid routes are flagged"""
        response = self.test_app.get('/something')
        self.assertEqual(response.status_code, 404)
