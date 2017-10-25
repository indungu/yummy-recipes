"""
This test suit contains the unittest for
the recipes and categories CRUD features
"""
from unittest import TestCase
from app.recipes import Categories, CATEGORIES, Recipes

CATEGORY = Categories()
RECIPE = Recipes()

class CategoriesTestCase(TestCase):
    """This class comprises of the categories unit tests"""

    def setUp(self):
        """Set up tests"""
        CATEGORIES.clear()

    def test_add_new_category(self):
        """Test that category can be added"""

        # Check if an instance of the category class is created
        self.assertIsInstance(CATEGORY, Categories)
        self.assertTrue(len(CATEGORIES) == 0)
        # Test if a category can be added
        CATEGORY.add_category('pies', 'for all the pie recipes')
        self.assertTrue(len(CATEGORIES) > 0)
        # Ensure that a category can only be created once
        duplicate = CATEGORY.add_category('pies', 'some other description')
        self.assertEqual(duplicate, "Sorry. Category already exists")

    def test_get_category(self):
        """Test that category can be retrieved"""

        CATEGORY.add_category('salads', 'some salad recipes')
        # test retrieving existing category
        retrived = CATEGORY.get_category('salads')
        self.assertEqual(retrived['name'], 'salads')
        # test retrieving non existing category
        retrived = CATEGORY.get_category('baking')
        self.assertEqual(retrived, 'Category does not exist.')

    def test_set_category(self):
        """Test that a category can be updated"""
        # test updating non existing category
        updated_category = CATEGORY.set_category('breakfast', 'my best breakfast recipes')
        self.assertEqual(updated_category, 'Category does not exist.')
        # Add category
        added_category = CATEGORY.add_category('cookies', 'my cookie recipes')
        self.assertTrue(added_category['name'] in CATEGORIES)
        updated_category = CATEGORY.set_category(
            'cookies', 'my favourite cookie recipes', [{'name': 'chocolate chip'}]
        )
        self.assertEqual(CATEGORIES['cookies'], updated_category)

    def test_delete_of_categories(self):
        """Testing that a category can be deleted"""

        self.assertTrue(len(CATEGORIES) == 0)
        self.assertTrue('pies' not in CATEGORIES)
        CATEGORY.add_category('pies', 'for all the pie recipes')
        assert 'pies' in CATEGORIES
        confirmation = CATEGORY.delete_category('pies')
        self.assertEqual(confirmation, "Removed successfully.")
        self.assertFalse('pies' in CATEGORIES)
        confirmation = CATEGORY.delete_category('pies')
        self.assertEqual(confirmation, "Category does not exist.")

class RecipesTestCase(TestCase):
    """This class comprises the unit tests for recipes"""
    def setUp(self):
        """Set up tests"""
        self.test_category = CATEGORY.add_category('pies', 'my pie recipes')
        self.add_recipe = RECIPE.add_recipe('pies', {
            'name': 'Apple Pie',
            'fun_fact': 'some fun fact',
            'ingredients': ['3 eggs', '4 cups of flour'],
            'description': 'how to prepare and serve'
        })

    def test_add_recipe(self):
        """Test that a recipe can be added for a particular category"""

        self.assertEqual(self.add_recipe, "Recipe added successfully.")
        self.assertTrue('Apple Pie' in CATEGORIES['pies']['recipes'])
        status = RECIPE.add_recipe('chicken', {
            'name': 'Chicken Tikka',
            'fun_fact': 'some fun fact',
            'ingredients': ['1 chicken breast', 'garam masala'],
            'description': 'how to prepare and serve'
        })
        self.assertEqual(status, 'Category does not exist.')

    def test_get_recipe(self):
        """Test if recipes can be retrieved"""
        # Get a non existent recipe
        status = RECIPE.get_recipe('lunch', 'caeser')
        self.assertEqual(status, 'Recipe does not exist')
        # Get an existent recipe
        status = RECIPE.get_recipe('pies', 'Apple Pie')
        self.assertTrue('Apple Pie' in CATEGORIES['pies']['recipes'])


    def test_set_recipe(self):
        """Test if recipes can be retrieved"""
        # Update a non existent recipe
        status = RECIPE.set_recipe('lunch', 'caeser', {
            'name': 'caesar salad', 'ingrediends': ['1 caesar salad', '1 professional chef'],
            'description': 'prep and serve'
        })
        self.assertEqual(status, 'Recipe does not exist')
        # Update an existent recipe
        assert 'Apple Pie' in CATEGORIES['pies']['recipes']
        status = RECIPE.set_recipe('pies', 'Apple Pie', {
            'name': 'Pot Pie', 'ingrediends': ['1 pot', '1 pie'],
            'description': 'prep and serve'
        })
        self.assertTrue('Pot Pie' in status)
        status = RECIPE.set_recipe('pies', 'Apple Pie', {
            'name': 'Pot Pie', 'ingrediends': ['1 pot', '1 pie'],
            'description': 'prep and serve'
        })
        self.assertEqual(status, 'Recipe does not exist')

    def test_delete_recipe(self):
        """Test that a recipe can be deleted"""
        # Confirm categories exist
        self.assertTrue(len(CATEGORIES) > 0)
        status = self.add_recipe
        self.assertTrue('Apple Pie' in CATEGORIES['pies']['recipes'])
        # Delete existing recipe from category
        status = RECIPE.delete_recipe('pies', 'Apple Pie')
        self.assertEqual(status, "Recipe deleted successfully!")
        # Delete non existing recipe from category
        status = RECIPE.delete_recipe('pies', 'Apple Pie')
        self.assertEqual(status, "Recipe does not exist!")
