"""Unit tests"""

import unittest

from flask import abort, url_for
from flask_testing import TestCase

from app import APP


class HomePageTestCase(unittest.TestCase):
    """Home page unit test"""

    # A user has heard about our amazing recipe app and decided to
    # check it out
    # They enter the url for the app in their browser and it
    # displays a welcome screen
    def test_index_decorator_renders_home_page_view(self):
        """Testing that the decorator renders the index.html template"""
        test_app = APP.test_client(self)
        response = test_app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # They notice that the browser title reads Yummy Recipes | Welcome
    def test_that_the_rendered_template_is_the_index_page(self):
        """Ensure that the right template is rendered"""
        test_app = APP.test_client(self)
        response = test_app.get('/', content_type='html/text')
        self.assertTrue(b'Yummy Recipes | Welcome' in response.data)
