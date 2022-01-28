from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    PasswordField, 
    SubmitField,
    BooleanField
)
from wtforms.validators import (
    DataRequired, 
    Email, 
    Length, 
    EqualTo, 
    ValidationError
)
from template.blueprints.users.models import User


class PasswordResetRequestForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[
            DataRequired(), 
            Email(), 
            Length(min=6, max=40)
        ]
    )
    submit = SubmitField('Reset Password')


class ChangeEmailForm(FlaskForm):
    email = StringField(
        'New Email', 
        validators=[
            DataRequired(), 
            Length(1, 64),
            Email()
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired()]
    )
    submit = SubmitField('Update Email Address')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered.')


class PasswordResetForm(FlaskForm):
    current_password = PasswordField(
        "Current Password", 
        validators=[DataRequired()]
    )
    new_password     = PasswordField(
        'New Password', 
        validators=[
            DataRequired(), 
            Length(min=8, max=25)
        ]
    )
    confirm = PasswordField(
        'Repeat Password', 
        validators=[
            DataRequired(), 
            EqualTo('new_password'), 
            Length(min=8, max=25)
        ]
    )
    submit = SubmitField('Reset Password')


class LoginForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[DataRequired()]
    )
    password = PasswordField(
        "Password", 
        validators=[DataRequired()]
    )
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    name = StringField(
        'Name', 
        validators=[DataRequired()]
    )
    username = StringField(
        'Username', 
        validators=[
            DataRequired(), 
            Length(min=6, max=40)
        ]
    )
    email = StringField(
        'Email', 
        validators=[
            DataRequired(), 
            Email(), 
            Length(min=6, max=40)
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            Length(min=8, max=25)
        ]
    )
    confirm = PasswordField(
        'Repeat Password', 
        validators=[
            DataRequired(), 
            EqualTo('password'), 
            Length(min=8, max=25)
        ]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
