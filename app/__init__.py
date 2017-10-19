"""Module initializer"""
from flask import Flask

# Initialize the application
APP = Flask(__name__)

# Import views
from app import views
