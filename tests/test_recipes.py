"""
This test suit contains the unittest for
the recipes and categories CRUD features
"""
from unittest import TestCase
from app.recipes import Categories, CATEGORIES, Recipes
from app import APP

CATEGORY = Categories()
RECIPE = Recipes()

class CategoriesTestCase(TestCase):
    """This class comprises of the categories unit tests"""

    def setUp(self):
        """Set up tests"""
        CATEGORIES.clear()
        self.user_email = "uim@yummy.io"
        self.username = "yummy_user"
        self.user_password = "some_pasw"
        APP.config['TESTING'] = True
        self.test_app = APP.test_client()

    def tearDown(self):
        """The following is done at the end of each test"""
        self.logout()

    def signup(self):
        """This is the signup helper method"""
        return self.test_app.post('/signup', data=dict(
            email=self.user_email,
            username=self.username,
            password=self.user_password,
            confirm=self.user_password
        ), follow_redirects=True)

    def login(self, email=None, password=None):
        """This method creates a login session"""
        if (email is None) and (password is None):
            return self.test_app.post('/login', data=dict(
                email=self.user_email,
                password=self.user_password
            ), follow_redirects=True)
        return self.test_app.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """This helper method clears a login session"""
        return self.test_app.get('/logout/', follow_redirects=True)

    def test_add_new_category(self):
        """Test that category can be added"""
        # Signup ans signin to activate session
        self.signup()
        self.login()
        # Check if an instance of the category class is created
        self.assertIsInstance(CATEGORY, Categories)
        self.assertTrue(len(CATEGORIES) == 0)
        # Test if a category can be added
        CATEGORY.add_category('pies', 'for all the pie recipes', self.user_email)
        self.assertTrue(len(CATEGORIES) > 0)
        # Ensure that a category can only be created once
        duplicate = CATEGORY.add_category('pies', 'some other description', self.user_email)
        self.assertEqual(duplicate, "Sorry. Category already exists")

    def test_get_category(self):
        """Test that category can be retrieved"""
        # Signup ans signin to activate session
        self.signup()
        self.login()
        CATEGORY.add_category('salads', 'some salad recipes', self.user_email)
        # test retrieving existing category
        retrived = CATEGORY.get_category('salads', self.user_email)
        self.assertEqual(retrived['name'], 'salads')
        # test retrieving non existing category
        retrived = CATEGORY.get_category('baking', self.user_email)
        self.assertEqual(retrived, 'Category does not exist.')

    def test_set_category(self):
        """Test that a category can be updated"""
        # test updating non existing category
        updated_category = CATEGORY.set_category('breakfast', 'my best breakfast recipes', self.user_email)
        self.assertEqual(updated_category, 'Category does not exist.')
        # Add category
        added_category = CATEGORY.add_category('cookies', 'my cookie recipes', self.user_email)
        self.assertTrue(added_category['name'] in CATEGORIES)
        updated_category = CATEGORY.set_category(
            'cookies', 'my favourite cookie recipes', self.user_email
        )
        self.assertEqual(CATEGORIES['cookies'], updated_category)

    def test_delete_of_categories(self):
        """Testing that a category can be deleted"""

        CATEGORY.add_category('pies', 'for all the pie recipes', self.user_email)
        assert 'pies' in CATEGORIES
        confirmation = CATEGORY.delete_category('pies', self.user_email)
        self.assertEqual(confirmation, "Removed successfully.")
        self.assertFalse('pies' in CATEGORIES)
        confirmation = CATEGORY.delete_category('pies', self.user_email)
        self.assertEqual(confirmation, "Category does not exist.")

class RecipesTestCase(TestCase):
    """This class comprises the unit tests for recipes"""
    def setUp(self):
        """Set up tests"""
        self.test_category = CATEGORY.add_category('pies', 'my pie recipes', 'uin@yummy.io')
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
        # Get a non existent recipe from a non existent category
        status = RECIPE.get_recipe('lunch', 'caeser')
        self.assertEqual(status, 'Recipe does not exist')
        # Get a non existent recipe from an existing category
        status = RECIPE.get_recipe('pies', 'caeser')
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
