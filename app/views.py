"""Views module"""
import sys
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, session

from app import APP
from .forms import SignupForm, LoginForm, CategoryForm, RecipeForm
from .users import User
from .recipes import CATEGORIES, Categories, Recipes

USER = User()
CATEGORY = Categories()
RECIPE = Recipes()

APP.secret_key = "Myl1TtL34cr3t"

session = {}

def is_authorized(function):
    """
    Thus creates a wrapper function decorator that checks user authorization
    """
    @wraps(function)
    def authorizer(*args, **kwargs):
        """Confirms user is not on an active session"""
        if 'logged_in' not in session:
            flash('Sorry, you need to be logged in to view this', 'warning')
            return redirect(url_for('login'))
        return function(*args, **kwargs)
    return authorizer

@APP.route('/')
def index():
    """Index view route"""
    title = "Welcome"
    return render_template('index.html', title=title)

@APP.route('/signup', methods=['GET', 'POST'])
def signup():
    """signup view route"""
    title = "Sign Up"
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        USER.add_user(form.email.data, form.username.data, form.password.data)
        return redirect(url_for('login'))
    return render_template('signup.html', title=title, form=form)

@APP.route('/login', methods=['GET', 'POST'])
def login():
    """login view route"""
    title = "Login"
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = USER.get_user(form.email.data, form.password.data)
        if user == "User not found!":
            flash('Invalid user!')
            return redirect(url_for('login'))
        elif user["email"] == form.email.data:
            session["logged_in"] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html', title=title, form=form)

@APP.route('/logout/')
@is_authorized
def logout():
    """logout route"""
    session.pop('logged_in')
    flash('You were logged out successfully')
    return redirect(url_for('login'))

@APP.route('/dashboard', methods=['GET', 'POST'])
@is_authorized
def dashboard():
    """route to dashboard view"""
    title = "Dashboard"
    form = CategoryForm()
    form_rec = RecipeForm()
    if request.method == 'POST' and form.validate():
        CATEGORY.add_category(form.name.data, form.description.data)
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html',
                           title=title,
                           form=form,
                           form_rec=form_rec,
                           categories=CATEGORIES
                          )

@APP.route('/add_recipe', methods=['GET', 'POST'])
@is_authorized
def add_recipe():
    """Adds a new recipe and redirects to dash"""
    form_rec = RecipeForm()
    if request.method == 'POST' and form_rec.validate():
        recipe = {
            'name': form_rec.name.data,
            'fun_fact': form_rec.fun_fact.data,
            'ingredients': form_rec.ingredients.data,
            'directions': form_rec.description.data
        }
        confirmation = RECIPE.add_recipe(form_rec.category.data, recipe)
        flash(confirmation)
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

@APP.route('/edit_category/<name>', methods=['GET', 'POST'])
@is_authorized
def edit_category(name):
    """Handles the category edit"""
    form = CategoryForm()
    if request.method == 'GET':
        category = CATEGORY.get_category(name)
        if category == 'Category does not exist.':
            flash(category)
            return redirect(url_for('dashboard'))
        form.name.data = category['name']
        form.description.data = category['description']
        return render_template('edit_category.html', form=form)
    if form.validate():
        mod_category = CATEGORY.set_category(form.name.data, form.description.data)
        print(mod_category, file=sys.stdout)
        if mod_category == 'Category does not exist.':
            flash('Sorry, Category does not exist.')
            return redirect(url_for('dashboard'))
        flash('Category updated successfully')
        return redirect(url_for('dashboard'))
