from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasklib.models import Book, Library, User

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

    def fill_choices(self):
        choices = list()
        tables = Library.query.all()
        for lib in tables:
            choices.append((lib.id, lib.city+" "+lib.street+" "+str(lib.housenumber)))
        return choices
      

    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
    autor = StringField('Autor', validators=[DataRequired(), Length(min=2, max=40)])
    publisher = StringField('Publisher', validators=[DataRequired(), Length(min=2, max=40)])
    tag = StringField('Tag', validators=[DataRequired(), Length(min=2, max=40)])
    library = SelectField('Library', validators=[DataRequired()], choices=[])
    img = StringField('Image', validators=[DataRequired(), Length(min=2, max=40)])

    submit = SubmitField('Add')
    
class ManageVotes(FlaskForm):
    def fill_choices_votes(self):
        choices = list()
        tables = Library.query.all()
        for lib in tables:
            choices.append((lib.id, lib.city+" "+lib.street+" "+str(lib.housenumber)))
        return choices
    
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
    autor = StringField('Autor', validators=[DataRequired(), Length(min=2, max=40)])
    publisher = StringField('Publisher', validators=[DataRequired(), Length(min=2, max=40)])
    tag = StringField('Tag', validators=[DataRequired(), Length(min=2, max=40)])
    library = SelectField('Library', validators=[DataRequired()], choices=[])

    submit = SubmitField('Add')

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

class OrderBookForm(FlaskForm):
      
    id = IntegerField('ID of Book to Order',validators=[DataRequired()])
    number_of = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Order')
    def validate_id(self, id):
        book = Book.query.filter_by(id=id.data).first()
        if not book:
            raise ValidationError('Book with given ID does not exist. Please set valid Book ID.')
    


            

