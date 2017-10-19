"""Main App module"""

from flask import Flask, render_template, url_for

APP = Flask(__name__)

@APP.route('/')
def index():
    return render_template('index.html')
