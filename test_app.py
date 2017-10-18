"""Unit tests"""

import unittest
from app.app import APP

class HomePageTestCase(unittest.TestCase):
    """Home page unit test"""

    # A user has heard about our amazing recipe app and decided to
    # check it out
    # They enter the url for the app in their browser and it
    # displays a welcome screen
    def test_index_decorator_home_page_view(self):
        """Testing that the decorator renders the index.html template"""
        test_app = APP.test_client(self)
        response = test_app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
