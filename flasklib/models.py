from datetime import datetime
from flasklib import db, login_manager
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role_name = db.Column(db.String(40),db.ForeignKey('role.name'))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

    users = db.relationship('User', backref='ro_user')

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(40), nullable=False)
    street = db.Column(db.String(40), nullable=False)
    housenumber = db.Column(db.Integer, nullable=False)

    books = db.relationship('Book', backref='all_books')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    autor = db.Column(db.String(40), nullable=False)
    publisher = db.Column(db.String(40), nullable=False)
    tag = db.Column(db.String(40), nullable=False)
    
    #reservations = db.relationship('Reservation', backref='reservations')
    library = db.Column(db.Integer, db.ForeignKey('library.id'))

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.ro_user.name == "admin":
                return True
            else:
                return False
        else:
            return False

    def inaccessible_callback(self,name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.ro_user.name == "admin":
                return True
            else:
                return False
        else:
            return False
