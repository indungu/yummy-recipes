"""Routes testing suite."""

from unittest import TestCase

from app import APP
from app.users import User, USERS

class RoutesTestCase(TestCase):
    """This class contains all the test methods used for testing"""

    def setUp(self):
        """set up for each test"""
        APP.config['TESTING'] = True
        APP.config['WTF_CSRF_ENABLED'] = False
        self.test_app = APP.test_client()
        self.user_email = "win@user.me"
        self.username = "user"
        self.user_password = "password"
        self.user = User(self.user_email, self.username, self.user_password)
        self.user.add_user()

    def tearDown(self):
        """The following is done at the end of each test"""
        self.logout()
        USERS.clear()

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

    def add_category(self):
        """This helper method adds a test category"""
        return self.test_app.post('/dashboard', data=dict(
            name='Pies',
            description='Classic American pies',
            owner=self.user_email
        ), follow_redirects=True)

    def add_recipe(self):
        """This helper method adds a test recipe"""
        return self.test_app.post('/add_recipe/Pies', data=dict(
            category='Pies',
            name='Apple Pie',
            fun_fact='Pilgrims thanksgiving gift to the Native Americans',
            ingredients='Some of this\r\nSome of that',
            description='Do this\r\nThen that\r\nThen the other\r\nPrepare and serve with love'
        ), follow_redirects=True)

    # Ensure that welcome page loads on the root route
    def test_root_route(self):
        """Tests whether the root url"""
        # Ensure that landing page opens for non logged in user
        reponse = self.test_app.get('/')
        self.assertEqual(reponse.status_code, 200)
        self.assertIn(b'Yummy Recipes | Welcome', reponse.data)
        # Ensure that landing page redirect to dashboard
        # for logged in user
        self.signup()
        self.login()
        reponse = self.test_app.get('/', follow_redirects=True)
        self.assertEqual(reponse.status_code, 200)
        self.assertIn(b'Yummy Recipes | Dashboard', reponse.data)

    def test_signup_route(self):
        """Test if the signup route/url opens"""
        response = self.test_app.get('/signup')
        self.assertIn(b'Yummy Recipes | Sign Up', response.data)
        # Ensure users are redicted to login page after successful signup
        self.user.delete_user()
        response = self.signup()
        self.assertIn(b'Yummy Recipes | Login', response.data)
        # Assert the same email cannot register a new account
        response = self.signup()
        self.assertIn(b'Sorry, that email is already registered.', response.data)
        # Ensure that logged in users can't access signup page
        self.login()
        response = self.test_app.get('/signup', follow_redirects=True)
        self.assertIn(b'Yummy Recipes | Dashboard', response.data)

    def test_login_route(self):
        """Test if the login route/url opens"""
        # Ensure user can navigate to login page
        response = self.test_app.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        # Ensure user can login with valid credentials
        self.signup()
        response = self.login()
        self.assertIn(b'Yummy Recipes | Dashboard', response.data)
        self.logout()
        # Ensure user can't login with invalid credentials
        # Invalid/none existing email
        response = self.login('some@email.com', self.user_password)
        self.assertIn(b'Invalid/Unregistered user! Sign Up to create account.', response.data)
        self.assertIn(b'Yummy Recipes | Sign Up', response.data)
        # Wrong password
        response = self.login(self.user_email, "fake_pass")
        self.assertIn(b'Password error. Please enter the correct details.\n', response.data)
        self.assertIn(b'Yummy Recipes | Login', response.data)


    def test_logout_route(self):
        """Test that user can logout"""
        self.signup()
        self.login()
        # Ensure that logged in user is succesfully logged out
        response = self.logout()
        self.assertIn(b'You were logged out successfully', response.data)

    def test_dashboard_route(self):
        """When user is not authorized"""
        # Ensure user is redirected to login view if they don't have an active session
        response = self.test_app.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        # Ensure that user can access dashboard upon login
        self.signup()
        response = self.login()
        self.assertIn(
            b'Yummy Recipes | Dashboard',
            response.data
        )
        # Ensure that a user can add a new category
        response = self.add_category()
        self.assertIn(b'Pies', response.data)

    def test_add_recipe_route(self):
        """Tests for the add recipe route"""
        self.signup()
        self.login()
        # Ensure that explicit entry of this URL in browser redirects to dashboard
        # whilst user is in session
        response = self.test_app.get('/add_recipe/Pies', follow_redirects=True)
        self.assertIn(b'Yummy Recipes | Add Recipe', response.data)
        # Ensure that user can only add a recipe to existing category
        response = self.add_recipe()
        self.assertIn(b'Category does not exist.', response.data)
        # Create/add test category
        self.add_category()
        response = self.add_recipe()
        self.assertIn(b'Recipe added successfully.', response.data)

    def test_edit_category_route(self):
        """Tests for the edit category route"""
        self.signup()
        self.login()
        self.add_category()
        # Ensure that the edit category view loads
        response = self.test_app.get('/edit_category/Pies', follow_redirects=True)
        self.assertIn(b'Yummy Recipes | Edit Category', response.data)
        # Ensure that incorrect categories are flagged
        response = self.test_app.get('/edit_category/Cookies', follow_redirects=True)
        self.assertIn(b'Category does not exist.', response.data)
        # Ensure that existing category can be updated
        response = self.test_app.post('/edit_category/Pies', data=dict(
            name='Pies',
            description='Good old pie recipes',
            owner=self.user_email
        ), follow_redirects=True)
        self.assertIn(b'Good old pie recipes', response.data)
        # Ensure that existing category name can be changed on post request
        response = self.test_app.post('/edit_category/Pies', data=dict(
            name='Cookies',
            description='Good old cookie recipes',
            owner=self.user_email
        ), follow_redirects=True)
        self.assertIn(b'Yummy Recipes | Dashboard', response.data)
        self.assertIn(b'Category updated successfully\n', response.data)

        # Ensure that existing category name can.t be changed with invalid data on post request
        response = self.test_app.post('/edit_category/Pies', data=dict(
            name='Coo',
            description='Good old cookie recipes',
            owner=self.user_email
        ), follow_redirects=True)
        self.assertIn(b'Yummy Recipes | ', response.data)
        self.assertIn(b'Invalid form details, please check your category name.\n', response.data)

    def test_delete_category_route(self):
        """Tests for the category delete feature route"""
        # Instanciate test
        self.signup()
        self.login()
        self.add_category()
        # Ensure that non-existing categories are flagged
        response = self.test_app.get('/delete_category/Cookies', follow_redirects=True)
        self.assertIn(b'Sorry, category Cookies does not exist.', response.data)
        # Ensure that category supplied is deleted
        response = self.test_app.get('/delete_category/Pies', follow_redirects=True)
        self.assertIn(b'Category Pies was removed successfully.', response.data)

    def test_edit_recipe_route(self):
        """Tests for the edit category route"""
        # Initialize
        self.signup()
        self.login()
        self.add_category()
        self.add_recipe()
        # Ensure that the edit recipe view loads
        response = self.test_app.get('/edit_recipe/Pies/Apple_Pie', follow_redirects=True)
        self.assertIn(b'Yummy Recipes | Edit Recipe', response.data)
        # Ensure that incorrect/non-existent recipes are flagged
        response = self.test_app.get('/edit_recipe/Cookies/Chocolate_Chip', follow_redirects=True)
        self.assertIn(b'Recipe does not exist', response.data)
        # Ensure that selected recipe can be updated
        response = self.test_app.post('/edit_recipe/Pies/Apple_Pie', data=dict(
            category='Pies',
            name='Pot Pie',
            fun_fact='Yes, it is indeed a pie with pot',
            ingredients='Pot\nGoogle\nPie',
            description='Prepare with care, serve with lots of love and other smaller pies'
        ), follow_redirects=True)
        self.assertIn(b'Recipe updated successfully.', response.data)
        # Ensure that existing recipes can't be updated with invalid data
        response = self.test_app.post('/edit_recipe/Pies/Apple_Pie', data=dict(
            category='Pies',
            name='Pot Pie',
            fun_fact='Yes, it is indeed a pie with pot',
            ingredients='',
            description=''
        ), follow_redirects=True)
        self.assertIn(b'Sorry you provided invalid values, Please try again.', response.data)
        # Ensure incorrect/non-existent recipes can't be updated
        response = self.test_app.post('/edit_recipe/Pies/Chicken_Pot_Pie', data=dict(
            category='Pies',
            name='Chicken Pot Pie',
            fun_fact='Yes, it is indeed a pie with pot',
            ingredients='Pot\nGoogle\nPie',
            description='Prepare with care, serve with lots of love and other smaller pies'
        ), follow_redirects=True)
        self.assertIn(b'Yummy Recipes | Dashboard', response.data)
        self.assertIn(b'Sorry, recipe does not exist.', response.data)
        # Ensure that existing recipe can't not be altered from another
        # recipes edit request
        self.test_app.post('/add_recipe/Pies', data=dict(
            category='Pies',
            name='Chicken Pot Pie',
            fun_fact='Pilgrims thanksgiving gift to the Native Americans',
            ingredients='Some of this\r\nSome of that',
            description='Do this\r\nThen that\r\nThen the other\r\nPrepare and serve with love'
        ), follow_redirects=True)
        response = self.test_app.post('/edit_recipe/Pies/Chicken_Pot_Pie', data=dict(
            category='Pies',
            name='Pot Pie',
            fun_fact='Yes, it is indeed a pie with pot',
            ingredients='Pot\nGoogle\nPie',
            description='Prepare with care, serve with lots of love and other smaller pies'
        ), follow_redirects=True)
        self.assertIn(
            b"The name provided is of an existing recipe. Please choose another", response.data
        )

    def test_delete_recipe_route(self):
        """Tests for the category delete feature route"""
        # Instanciate test
        self.signup()
        self.login()
        self.add_category()
        self.add_recipe()
        # Ensure that non-existing recipes are flagged
        response = self.test_app.get('/delete_recipe/Pies/Chocolate_Chip', follow_redirects=True)
        self.assertIn(b'Sorry, recipe Chocolate_Chip does not exist.', response.data)
        # Ensure that recipe supplied is deleted
        response = self.test_app.get('/delete_recipe/Pies/Apple_Pie', follow_redirects=True)
        self.assertIn(b'Recipe Apple_Pie was removed successfully.', response.data)

    def test_invalid_routes(self):
        """Test if invalid routes are flagged"""
        response = self.test_app.get('/something')
        self.assertEqual(response.status_code, 404)
