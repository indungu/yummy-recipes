"""Views module"""
from functools import wraps
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app import APP
from .forms import SignupForm, LoginForm, CategoryForm, RecipeForm
from .users import User, USERS
from .recipes import CATEGORIES, Categories, Recipes


CATEGORY = Categories()
RECIPE = Recipes()

APP.secret_key = "Myl1TtL34cr3t"

def is_authorized(function):
    """
    Thus creates a wrapper function decorator that checks user authorization
    """
    @wraps(function)
    def authorizer(*args, **kwargs):
        """Confirms user is not on an active session"""
        if 'user' not in session:
            flash('Sorry, you need to be logged in to view this', 'warning')
            return redirect(url_for('login'))
        return function(*args, **kwargs)
    return authorizer

@APP.route('/')
def index():
    """Index view route"""
    title = "Welcome"
    if "logged_in" not in session:
        return render_template('index.html', title=title)
    if session['logged_in']:
        return redirect(url_for('dashboard'))

@APP.route('/signup', methods=['GET', 'POST'])
def signup():
    """signup view route"""
    title = "Sign Up"
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.email.data, form.username.data, form.password.data)
        status = user.add_user()
        flash(status)
        if status == "Sorry, that email is already registered.":
            return redirect(url_for('signup'))
        return redirect(url_for('login'))
    elif "logged_in" not in session:
        return render_template('signup.html', title=title, form=form)
    if session['logged_in']:
        return redirect(url_for('dashboard'))

@APP.route('/login', methods=['GET', 'POST'])
def login():
    """ login view route """
    title = "Login"
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        if email not in USERS:
            flash('Invalid/Unregistered user! Sign Up to create account.')
            return redirect(url_for('signup'))
        elif check_password_hash(USERS[email].password, form.password.data):
            session['user'] = email
            session['username'] = USERS[email].username
            session["logged_in"] = True
            return redirect(url_for('dashboard', user=session['username']))
        flash('Password error. Please enter the correct details.')
        return redirect(url_for('login'))
    return render_template('login.html', title=title, form=form)

@APP.route('/logout/')
@is_authorized
def logout():
    """logout route"""
    session.clear()
    flash('You were logged out successfully')
    return redirect(url_for('login'))

@APP.route('/dashboard', methods=['GET', 'POST'])
@is_authorized
def dashboard():
    """route to dashboard view"""

    title = "Dashboard"
    form = CategoryForm()
    if request.method == 'POST' and form.validate():
        status = CATEGORY.add_category(form.name.data, form.description.data, session['user'])
        if status == "Sorry. Category already exists":
            flash(status)
        else:
            return redirect(url_for('dashboard'))
    user_categories = {}
    for category in CATEGORIES:
        if CATEGORIES[category]['owner'] == session['user']:
            user_categories[category] = CATEGORIES[category]
    return render_template('dashboard.html',
                           title=title,
                           form=form,
                           user=session['username'],
                           categories=user_categories
                          )

@APP.route('/add_recipe/<category>', methods=['GET', 'POST'])
@is_authorized
def add_recipe(category):
    """Adds a new recipe and redirects to dash"""
    title = "Add Recipe"
    form = RecipeForm()
    if request.method == 'POST' and form.validate():
        recipe = {
            'category': category,
            'name': '_'.join(form.name.data.split()),
            'fun_fact': form.fun_fact.data,
            'ingredients': form.ingredients.data.split('\r\n'),
            'description': form.description.data.split('\r\n')
        }
        confirmation = RECIPE.add_recipe(category, recipe)
        flash(confirmation)
        return redirect(url_for('dashboard'))
    return render_template('add_recipe.html', title=title, form=form, category=category)

@APP.route('/edit_category/<name>', methods=['GET', 'POST'])
@is_authorized
def edit_category(name):
    """Handles the category edit"""
    title = "Edit Category"
    form = CategoryForm(request.form)
    if request.method == 'GET':
        category = CATEGORY.get_category(name, session['user'])
        if category == 'Category does not exist.':
            flash(category)
            return redirect(url_for('dashboard'))
        form.name.data = category['name']
        form.description.data = category['description']
        return render_template('edit_category.html', form=form, title=title, name=name)
    if form.validate():
        updated_category = CATEGORY.set_category(name, form.description.data, session['user'])
        updated_category['name'] = form.name.data
        for recipe in CATEGORY.recipes:
            if CATEGORY.recipes[recipe]['category'] == name: # pragma: no cover
                CATEGORY.recipes[recipe]['category'] = form.name.data
        flash('Category updated successfully')
        CATEGORIES[form.name.data] = CATEGORIES.pop(name)
        return redirect(url_for('dashboard'))
    flash('Invalid form details, please check your category name.')
    return redirect(url_for('edit_category', name=name))

@APP.route('/delete_category/<name>')
@is_authorized
def delete_category(name):
    """This handles the delete feature for categories"""
    category = CATEGORY.get_category(name, session['user'])
    if category == 'Category does not exist.':
        flash('Sorry, category '+name+' does not exist.')
        return redirect(url_for('dashboard'))
    CATEGORIES.pop(name)
    recipes_to_delete = []
    for recipe in CATEGORY.recipes:
        if CATEGORY.recipes[recipe]['category'] == name:
            recipes_to_delete.append(recipe)
    for item in recipes_to_delete:
        del CATEGORY.recipes[item]
    flash('Category '+name+' was removed successfully.')
    return redirect(url_for('dashboard'))

@APP.route('/edit_recipe/<category>/<name>', methods=['GET', 'POST'])
@is_authorized
def edit_recipe(category, name):
    """Handles the category edit"""
    title = "Edit Recipe"
    form = RecipeForm()
    if request.method == 'GET':
        recipe = RECIPE.get_recipe(category, name)
        if recipe == 'Recipe does not exist':
            flash(recipe)
            return redirect(url_for('dashboard'))
        form.name.data = recipe['name']
        form.fun_fact.data = recipe['fun_fact']
        form.ingredients.data = "\r\n".join(recipe['ingredients'])
        form.description.data = "\r\n".join(recipe['description'])
        return render_template('edit_recipe.html', form=form, title=title, category=category)
    if form.validate_on_submit():
        mod_recipe = RECIPE.set_recipe(category, name, {
            'name': '_'.join(form.name.data.split()),
            'fun_fact': form.fun_fact.data,
            'ingredients': form.ingredients.data.split('\r\n'),
            'description': form.description.data.split('\r\n')
        })
        if mod_recipe == 'Recipe does not exist':
            flash('Sorry, recipe does not exist.')
            return redirect(url_for('dashboard'))
        flash('Recipe updated successfully.')
        return redirect(url_for('dashboard'))
    flash('Sorry you provided invalid values, Please try again.')
    return redirect(url_for('edit_recipe', category=category, name=name))

@APP.route('/delete_recipe/<category>/<name>')
@is_authorized
def delete_recipe(category, name):
    """This handles the delete feature for categories"""
    recipe = RECIPE.get_recipe(category, name)
    if recipe == 'Recipe does not exist':
        flash('Sorry, recipe '+name+' does not exist.')
        return redirect(url_for('dashboard'))
    CATEGORIES[category]['recipes'].pop(name)
    flash('Recipe '+name+' was removed successfully.')
    return redirect(url_for('dashboard'))
