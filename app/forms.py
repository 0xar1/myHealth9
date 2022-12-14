from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField,DateTimeField, SubmitField, validators,ValidationError,SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from datetime import datetime

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(),  Length(min=6,max=50)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(), Length(max=50)]) 
    fullname = StringField('Full Name',validators=[InputRequired(), Length(max=50)]) 
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(min=6,max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(max=50)])
    confirm = PasswordField('Confirm Password',validators=[InputRequired()])
    submit = SubmitField('Register')

