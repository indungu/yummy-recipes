"""Views module"""
import sys
from flask import render_template, request, redirect, url_for

from app import APP
from .forms import SignupForm, LoginForm
from .users import User, USERS

USER = User()

APP.secret_key = "Myl1TtL34cr3t"

@APP.route('/')
def index():
    """Index view route"""
    return render_template('index.html')

@APP.route('/signup', methods=['GET', 'POST'])
def signup():
    """signup view route"""
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        user = USER.add_user(form.email.data, form.username.data, form.password.data)
        print(user, file=sys.stdout)
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@APP.route('/login', methods=['GET', 'POST'])
def login():
    """login view route"""
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = USER.get_user(form.email.data, form.password.data)
        if user == "user not found":
            return render_template(url_for('login'))
        elif user["email"] == form.email.data:
            print(user.email, file=sys.stdout)
            return render_template(url_for('dashboard'))

    return render_template('login.html', form=form)

@APP.route('/dashboard')
def dashboard():
    """route to dashboard view"""
    return render_template('dashboard.html')
