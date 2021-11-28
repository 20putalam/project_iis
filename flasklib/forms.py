from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasklib.models import Library, User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class AddBook(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
    autor = StringField('Autor', validators=[DataRequired(), Length(min=2, max=40)])
    publisher = StringField('Publisher', validators=[DataRequired(), Length(min=2, max=40)])
    tag = StringField('Tag', validators=[DataRequired(), Length(min=2, max=40)])
    choices = list()
    library = SelectField('Library', validators=[DataRequired()], choices=choices)
    submit = SubmitField('Add')

    def fill_choices(self, library, choices):
        for lib in Library.query.all():
            choices.append((lib.id, lib.city+" "+lib.street+" "+str(lib.housenumber)))
    


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class AddUsersForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Add User')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class AddLibrariesForm(FlaskForm):

    city = StringField('City',validators=[DataRequired(), Length(min=1, max=40)])
    street = StringField('Street',validators=[DataRequired(), Length(min=1, max=40)])
    housenumber = IntegerField('Housenumber', validators=[DataRequired()])
    submit_add = SubmitField('Add')

class ChangeLibrariesForm(FlaskForm):

    id = IntegerField('ID of Library to change',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired(), Length(min=1, max=40)])
    street = StringField('Street',validators=[DataRequired(), Length(min=1, max=40)])
    housenumber = IntegerField('Housenumber', validators=[DataRequired()])
    submit_change = SubmitField('Change')

    


            

