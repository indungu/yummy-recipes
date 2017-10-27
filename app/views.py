"""Views module"""

from functools import wraps
from flask import render_template, request, redirect, url_for, flash, session

from app import APP
from .forms import SignupForm, LoginForm
from .users import User

USER = User()

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

@APP.route('/dashboard')
@is_authorized
def dashboard():
    """route to dashboard view"""
    title = "Dashboard"
    flash('Welcome, you were successfully logged in')
    return render_template('dashboard.html', title=title)
