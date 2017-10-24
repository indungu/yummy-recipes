"""A module for forms used"""
from wtforms import StringField, PasswordField, validators, SubmitField
from flask_wtf import FlaskForm

class SignupForm(FlaskForm):
    """The signup form"""
    email = StringField(
        'Email Address',
        [
            validators.data_required(),
            validators.Length(min=6, max=35),
            validators.email(message="Invalid email address")
        ]
    )
    username = StringField(
        'Username', [validators.data_required(), validators.Length(min=4, max=25)]
    )
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password', [validators.data_required()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    """The signup form"""
    email = StringField('Email Address', [
        validators.data_required(),
        validators.email(message="Invalid email address")
    ])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])
    login = SubmitField("Login")
