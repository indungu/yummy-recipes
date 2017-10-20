"""Module initializer"""
from flask import Flask

# Initialize the application
APP = Flask(__name__, instance_relative_config=True)

# Import views
from app import views

# load the default configuration
APP.config.from_object('config')
