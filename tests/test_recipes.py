"""
This test suit contains the unittest for
the recipes and categories CRUD features
"""
from unittest import TestCase
from app.recipes import Categories, CATEGORIES

CATEGORY = Categories()

class CategoriesTestCase(TestCase):
    """This class comprises of the categories unit tests"""

    def test_add_new_category(self):
        """Test that category can be added"""

        # Check if an instance of the category class is created
        self.assertIsInstance(CATEGORY, Categories)
        # Test if a category can be added
        test_category = CATEGORY.add_category('pies', 'for all the pie recipes')
        self.assertTrue(test_category['name'] in CATEGORIES)
        # Ensure that a category can only be created once
        duplicate = CATEGORY.add_category('pies', 'some other description')
        self.assertEqual(duplicate, "Sorry. Category already exists")

    def test_get_category(self):
        """Test that category can be retrieved"""

        CATEGORY.add_category('salads', 'some salad recipes')
        # test retrieving existing category
        retrived = CATEGORY.get_category('salads')
        self.assertEqual(retrived['name'], 'salads')
        retrived = CATEGORY.get_category('baking')
        self.assertEqual(retrived, 'Category does not exist.')

    def test_update_category(self):
        """Test that a category can be updated"""

        updated_category = CATEGORY.set_category('breakfast', 'my best breakfast recipes')
        self.assertEqual(updated_category, 'Category does not exist.')
        added_category = CATEGORY.add_category('cookies', 'my cookie recipes')
        self.assertTrue(added_category['name'] in CATEGORIES)
        updated_category = CATEGORY.set_category(
            'cookies', 'my favourite cookie recipes', [{'name': 'chocolate chip'}]
        )
        self.assertEqual(CATEGORIES['cookies'], updated_category)

    def test_delete_of_categories(self):
        """Testing that a category can be deleted"""

        # confirm that category exists
        self.assertTrue(len(CATEGORIES) > 0)
        self.assertTrue('pies' in CATEGORIES)
        confirmation = CATEGORY.delete_category('pies')
        self.assertEqual(confirmation, "Removed successfully.")
        self.assertFalse('pies' in CATEGORIES)
        confirmation = CATEGORY.delete_category('pies')
        self.assertEqual(confirmation, "Category does not exist.")
