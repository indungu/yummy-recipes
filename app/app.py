"""Main App module"""

from flask import Flask, render_template, url_for

APP = Flask(__name__)

@APP.route('/')
def index():
    """Index view route"""
    return render_template('index.html')

@APP.route('/signup')
def signup():
    """signup view route"""
    return render_template('signup.html')

@APP.route('/login')
def login():
    """login view route"""
    return render_template('login.html')

@APP.route('/dashboard')
def dashboard():
    """route to dashboard view"""
    return render_template('dashboard.html')

