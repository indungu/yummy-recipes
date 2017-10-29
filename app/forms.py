"""A module for forms used"""
from wtforms import StringField, PasswordField, validators, SubmitField, TextAreaField
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

class CategoryForm(FlaskForm):
    """The new category form"""
    name = StringField('Name', [
        validators.data_required('Please name your category'),
        validators.length(min=4, max=10, message='Name should be 4-10 characters long')
    ])
    description = TextAreaField('Description', [
        validators.data_required('A description would be nice.'),
        validators.length(max=50, message='Description should be less than 50 characters long')
    ])

class RecipeForm(FlaskForm):
    """This defines the form for recipe manipulation"""
    category = StringField('Category', [
        validators.data_required(message='Enter a category please.')
    ])
    name = StringField('Name', [
        validators.data_required('A name for your recipe would be nice')
    ])
    fun_fact = StringField('Fun Fact')
    ingredients = TextAreaField('Ingredients', [
        validators.data_required('Some ingredients please')
    ])
    description = TextAreaField('Directions and Serving', [
        validators.data_required('How can I prepare this?')
    ])
