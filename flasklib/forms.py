from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.choices import SelectField
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
    library = StringField('Library', validators=[DataRequired(), Length(min=2, max=40)])
    submit = SubmitField('Přidat')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 

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

    def validate_library(self, city):
        par1 = Library.query.filter_by(city=city.data).first()
        #par2 = Library.query.filter_by(street==street.data).first()
        #par3 = Library.query.filter_by(housenumber==housenumber.data).first()
        if par1:
            raise ValidationError('That library already exists, please set valid information')
   

class ChangeLibrariesForm(FlaskForm):

    id = IntegerField('ID of Library to change',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired(), Length(min=1, max=40)])
    street = StringField('Street',validators=[DataRequired(), Length(min=1, max=40)])
    housenumber = IntegerField('Housenumber', validators=[DataRequired()])
    submit_change = SubmitField('Change')

    def validate_library_2(self, city, street, housenumber):
        par1 = Library.query.filter_by(city==city.data).first()
        par2 = Library.query.filter_by(street==street.data).first()
        par3 = Library.query.filter_by(housenumber==housenumber.data).first()
        if par1 and par2 and par3:
            raise ValidationError('That library already exists, please set valid information')
    


            

