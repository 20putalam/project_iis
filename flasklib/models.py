from datetime import datetime
from flasklib import db, login_manager
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    
    reservations = db.relationship('Reservation', backref='u_reserve')
    borrow = db.relationship('Borrowing', backref='u_borrow')

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
    
    number_of = db.Column(db.Integer, nullable=False)
    library = db.Column(db.Integer, db.ForeignKey('library.id'))
    
    reservations = db.relationship('Reservation', backref='b_reserve')
    borrow = db.relationship('Borrowing', backref='b_borrow')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    valid_until = db.Column(db.DateTime,  default=db.func.current_timestamp()+ '3 days')

class Borrowing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    valid_until = db.Column(db.DateTime,  default=db.func.current_timestamp()+ '30 days')

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
