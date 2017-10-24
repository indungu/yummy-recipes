"""Routes testing suite."""

from unittest import TestCase

from app import APP

class RoutesTestCase(TestCase):
    """This class contains all the test methods used for testing"""

    def setUp(self):
        """set up for each test"""
        self.test_app = APP.test_client()

    def test_root_route(self):
        """Tests whether the root url opens"""
        reponse = self.test_app.get('/')
        self.assertEqual(reponse.status_code, 200)

    def test_signup_route(self):
        """Test if the signup route/url opens"""
        response = self.test_app.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        """Test if the login route/url opens"""
        response = self.test_app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_route(self):
        """Test if dashboard route/url opens"""
        response = self.test_app.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_invalid_routes(self):
        """Test if invalid routes are flagged"""
        response = self.test_app.get('/something')
        self.assertEqual(response.status_code, 404)
