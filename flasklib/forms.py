from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasklib.models import User


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

class ManageUsersForm(FlaskForm):
    id = IntegerField('ID',validators=[DataRequired()])
    submit = SubmitField('Delete')
    
class UserRolesForm(FlaskForm):
    role = SelectField('Role',validators=[DataRequired()],choices=[1,2,3,4])
    submit = SubmitField('Set')

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
            

